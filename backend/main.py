import asyncio
from uuid import uuid4
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from database import engine, create_tables
from models import Job, Thumbnail
from services.generator import process_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateJobPayload(BaseModel):
    prompt: str
    num_thumbnail: int = 1
    headshot_url: str


class ThumbnailResponse(BaseModel):
    id: str
    job_id: str
    style_name: str
    image_url: str
    status: str
    error_message: str | None
    created_at: str


class JobResponse(BaseModel):
    id: str
    prompt: str
    num_thumbnail: int
    headshot_url: str
    status: str
    created_at: str
    thumbnails: list[ThumbnailResponse] = []


def _thumbnail_to_response(t: Thumbnail) -> ThumbnailResponse:
    return ThumbnailResponse(
        id=t.id,
        job_id=t.job_id,
        style_name=t.style_name,
        image_url=t.image_url,
        status=t.status,
        error_message=t.error_message,
        created_at=t.created_at.isoformat(),
    )


def _job_to_response(job: Job) -> JobResponse:
    return JobResponse(
        id=job.id,
        prompt=job.prompt,
        num_thumbnail=job.num_thumbnail,
        headshot_url=job.headshot_url,
        status=job.status,
        created_at=job.created_at.isoformat(),
        thumbnails=[_thumbnail_to_response(t) for t in (job.thumbnails or [])],
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/jobs")
def list_jobs():
    with Session(engine) as session:
        jobs = session.exec(
            select(Job)
            .options(selectinload(Job.thumbnails))
            .order_by(Job.created_at.desc())
        ).all()
        return [_job_to_response(j) for j in jobs]


@app.post("/api/jobs", status_code=201)
async def create_job(payload: CreateJobPayload):
    if payload.num_thumbnail < 1 or payload.num_thumbnail > 3:
        raise HTTPException(status_code=422, detail="num_thumbnail must be between 1 and 3")

    job = Job(
        id=str(uuid4()),
        prompt=payload.prompt,
        num_thumbnail=payload.num_thumbnail,
        headshot_url=payload.headshot_url,
        status="pending",
    )
    with Session(engine) as session:
        session.add(job)
        session.commit()
        session.refresh(job)
        # eager-load thumbnails while session is active
        stmt = (
            select(Job)
            .options(selectinload(Job.thumbnails))
            .where(Job.id == job.id)
        )
        job = session.exec(stmt).first()

    asyncio.create_task(process_job(job.id))

    return _job_to_response(job)


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    with Session(engine) as session:
        stmt = (
            select(Job)
            .options(selectinload(Job.thumbnails))
            .where(Job.id == job_id)
        )
        job = session.exec(stmt).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return _job_to_response(job)


@app.get("/api/jobs/{job_id}/thumbnails")
def get_job_thumbnails(job_id: str):
    with Session(engine) as session:
        thumbnails = session.exec(
            select(Thumbnail).where(Thumbnail.job_id == job_id)
        ).all()
        return [_thumbnail_to_response(t) for t in thumbnails]
