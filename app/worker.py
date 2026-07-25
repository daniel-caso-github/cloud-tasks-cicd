"""Worker consumidor de eventos SQS (ver wiki: worker-sqs).

Bucle receive -> process -> delete, con long polling y backoff cuando la cola está vacía.
Marca la Task correspondiente como `processed` en DynamoDB. Corre como proceso aparte, sin HTTP.
"""

import json
import logging
import time

from app.aws import sqs_client
from app.config import get_settings
from app.models import TaskStatus
from app.repositories import tasks_repository

logger = logging.getLogger("worker")

EMPTY_QUEUE_BACKOFF_SECONDS = 5
WAIT_TIME_SECONDS = 10


def _queue_url() -> str:
    return sqs_client().get_queue_url(QueueName=get_settings().events_queue)["QueueUrl"]


def process_message(body: str) -> None:
    """Procesa un mensaje: marca la Task como `processed`. Idempotente."""
    event = json.loads(body)
    task_id = event["task_id"]
    task = tasks_repository.get_task(task_id)
    if task is None:
        logger.warning("Task %s not found, skipping", task_id)
        return
    task.status = TaskStatus.PROCESSED
    tasks_repository.put_task(task)
    logger.info("Task %s marked as processed", task_id)


def run() -> None:
    """Bucle principal del worker: long polling sobre EVENTS_QUEUE."""
    queue_url = _queue_url()
    client = sqs_client()
    while True:
        response = client.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=WAIT_TIME_SECONDS
        )
        messages = response.get("Messages", [])
        if not messages:
            time.sleep(EMPTY_QUEUE_BACKOFF_SECONDS)
            continue
        for message in messages:
            process_message(message["Body"])
            client.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])


if __name__ == "__main__":
    logging.basicConfig(level=get_settings().log_level)
    run()
