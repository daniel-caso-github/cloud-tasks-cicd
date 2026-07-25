"""Acceso a SQS para eventos de tareas (ver wiki: worker-sqs, naming-recursos)."""

import json

from app.aws import sqs_client
from app.config import get_settings


def _queue_url() -> str:
    settings = get_settings()
    return sqs_client().get_queue_url(QueueName=settings.events_queue)["QueueUrl"]


def publish_task_created(task_id: str) -> None:
    message = {"event": "task_created", "task_id": task_id}
    sqs_client().send_message(QueueUrl=_queue_url(), MessageBody=json.dumps(message))
