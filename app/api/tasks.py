"""Router CRUD de tareas (ver wiki: microservicio-api, task)."""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, UploadFile

from app.models import Task, TaskCreate, TaskUpdate
from app.repositories import attachments_repository, events_repository, tasks_repository

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task = Task(title=payload.title, description=payload.description)
    tasks_repository.put_task(task)
    events_repository.publish_task_created(task.id)
    return task


@router.get("")
def list_tasks() -> list[Task]:
    return tasks_repository.list_tasks()


@router.get("/{task_id}")
def get_task(task_id: str) -> Task:
    task = tasks_repository.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}")
def update_task(task_id: str, payload: TaskUpdate) -> Task:
    task = tasks_repository.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = payload.status
    task.updated_at = datetime.now(timezone.utc).isoformat()
    tasks_repository.put_task(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str) -> None:
    task = tasks_repository.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_repository.delete_task(task_id)


@router.post("/{task_id}/attachment")
def upload_attachment(task_id: str, file: UploadFile) -> Task:
    task = tasks_repository.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    key = f"{task_id}/{file.filename}"
    attachments_repository.upload_attachment(key, file.file.read())
    task.attachment_key = key
    task.updated_at = datetime.now(timezone.utc).isoformat()
    tasks_repository.put_task(task)
    return task
