"""Modelos Pydantic de dominio (ver wiki: task)."""

from datetime import datetime, timezone
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    DONE = "done"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    attachment_key: str | None = None
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    status: TaskStatus
