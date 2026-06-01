from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel, Relationship


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Thumbnail(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    job_id: str = Field(foreign_key="job.id")
    style_name: str = Field(default="")
    image_url: str = Field(default="")
    status: str = Field(default="pending")
    error_message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=_now)

    job: Optional["Job"] = Relationship(back_populates="thumbnails")

    def __repr__(self) -> str:
        return f"<Thumbnail {self.id} status={self.status}>"


class Job(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    prompt: str = Field(default="")
    num_thumbnail: int = Field(default=1, ge=1, le=3)
    headshot_url: str = Field(default="")
    status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=_now)

    thumbnails: list["Thumbnail"] = Relationship(back_populates="job")

    def __repr__(self) -> str:
        return f"<Job {self.id} status={self.status}>"
