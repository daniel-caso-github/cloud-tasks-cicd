"""Fixtures compartidas: mock de AWS en memoria con moto (sin red)."""

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.aws import dynamodb_client, s3_client, sqs_client
from app.config import get_settings
from app.main import app


@pytest.fixture
def aws_mock():
    """Levanta DynamoDB/S3/SQS en memoria con moto y crea los recursos que la app espera."""
    with mock_aws():
        settings = get_settings()

        dynamodb_client().create_table(
            TableName=settings.tasks_table,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        s3_client().create_bucket(Bucket=settings.attachments_bucket)
        sqs_client().create_queue(QueueName=settings.events_queue)

        yield


@pytest.fixture
def client(aws_mock):
    """`TestClient` de FastAPI corriendo contra los mocks de moto."""
    return TestClient(app)
