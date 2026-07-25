"""Unit tests for the SQS worker (no network, moto mocks AWS)."""

import json

import pytest

from app.aws import sqs_client
from app.config import get_settings
from app.models import Task
from app.repositories import tasks_repository
from app.worker import process_message

pytestmark = pytest.mark.unit


def test_process_message_marks_task_as_processed(aws_mock):
    task = Task(title="Task 1")
    tasks_repository.put_task(task)
    message = json.dumps({"event": "task_created", "task_id": task.id})

    process_message(message)

    updated = tasks_repository.get_task(task.id)
    assert updated.status == "processed"


def test_run_receives_and_deletes_message(aws_mock):
    task = Task(title="Task 1")
    tasks_repository.put_task(task)

    queue_url = sqs_client().get_queue_url(QueueName=get_settings().events_queue)["QueueUrl"]
    sqs_client().send_message(
        QueueUrl=queue_url, MessageBody=json.dumps({"event": "task_created", "task_id": task.id})
    )

    response = sqs_client().receive_message(QueueUrl=queue_url, WaitTimeSeconds=0)
    messages = response.get("Messages", [])
    assert len(messages) == 1

    process_message(messages[0]["Body"])
    sqs_client().delete_message(QueueUrl=queue_url, ReceiptHandle=messages[0]["ReceiptHandle"])

    updated = tasks_repository.get_task(task.id)
    assert updated.status == "processed"

    empty = sqs_client().receive_message(QueueUrl=queue_url, WaitTimeSeconds=0)
    assert not empty.get("Messages")
