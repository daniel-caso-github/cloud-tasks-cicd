"""DynamoDB access for the Task entity (see wiki: task, naming-recursos)."""

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from app.aws import dynamodb_client
from app.config import get_settings
from app.models import Task

_serializer = TypeSerializer()
_deserializer = TypeDeserializer()


def _to_item(task: Task) -> dict:
    return {k: _serializer.serialize(v) for k, v in task.model_dump(mode="json").items()}


def _from_item(item: dict) -> Task:
    return Task(**{k: _deserializer.deserialize(v) for k, v in item.items()})


def put_task(task: Task) -> Task:
    """Create or replace a task (idempotent by `id`)."""
    dynamodb_client().put_item(TableName=get_settings().tasks_table, Item=_to_item(task))
    return task


def get_task(task_id: str) -> Task | None:
    response = dynamodb_client().get_item(
        TableName=get_settings().tasks_table, Key={"id": _serializer.serialize(task_id)}
    )
    item = response.get("Item")
    return _from_item(item) if item else None


def list_tasks() -> list[Task]:
    response = dynamodb_client().scan(TableName=get_settings().tasks_table)
    return [_from_item(item) for item in response.get("Items", [])]


def delete_task(task_id: str) -> None:
    dynamodb_client().delete_item(
        TableName=get_settings().tasks_table, Key={"id": _serializer.serialize(task_id)}
    )
