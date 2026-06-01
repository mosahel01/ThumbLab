import asyncio
from uuid import uuid4

from sqlmodel import Session

from database import engine
from models import Job, Thumbnail
from services.openai_service import generate_thumbnail
from services.imagekit_service import upload_image

STYLES = [
    "Modern YouTube thumbnail style — bold, vibrant colors, high contrast, eye-catching text overlay area",
    "Clean minimal style — soft lighting, neutral background, professional LinkedIn look",
    "Cinematic style — dramatic shadows, film grading, widescreen aspect",
]

async def process_job(job_id: str) -> None:
    """Process a thumbnail generation job: create thumbnail records, generate each via OpenAI, upload to ImageKit."""
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if not job:
            return

        job.status = "processing"
        session.add(job)
        session.commit()

        thumbnail_ids: list[str] = []

        for i in range(job.num_thumbnail):
            thumb = Thumbnail(
                id=str(uuid4()),
                job_id=job.id,
                style_name=STYLES[i] if i < len(STYLES) else STYLES[-1],
                status="processing",
            )
            session.add(thumb)
            session.commit()
            thumbnail_ids.append(thumb.id)

        for thumb_id in thumbnail_ids:
            await _process_single_thumbnail(job, thumb_id)

        with Session(engine) as final_session:
            final_job = final_session.get(Job, job_id)
            if final_job:
                all_completed = all(
                    t.status == "completed" or t.status == "failed"
                    for t in final_job.thumbnails
                )
                if all_completed:
                    final_job.status = "completed" if any(
                        t.status == "completed" for t in final_job.thumbnails
                    ) else "failed"
                    final_session.add(final_job)
                    final_session.commit()


async def _process_single_thumbnail(job: Job, thumb_id: str) -> None:
    """Generate a single thumbnail image and upload it to ImageKit. Marks the thumbnail as completed or failed."""
    try:
        with Session(engine) as session:
            thumb = session.get(Thumbnail, thumb_id)
            if not thumb:
                return

        image_bytes = await generate_thumbnail(
            prompt=job.prompt,
            style_prompt=thumb.style_name,
            headshot_url=job.headshot_url,
        )

        url = upload_image(
            file_bytes=image_bytes,
            file_name=f"thumb_{thumb_id}.png",
            folder=f"jobs/{job.id}",
        )

        with Session(engine) as session:
            thumb = session.get(Thumbnail, thumb_id)
            if thumb:
                thumb.status = "completed"
                thumb.image_url = url
                session.add(thumb)
                session.commit()

    except Exception as exc:
        with Session(engine) as session:
            thumb = session.get(Thumbnail, thumb_id)
            if thumb:
                thumb.status = "failed"
                thumb.error_message = str(exc)
                session.add(thumb)
                session.commit()
