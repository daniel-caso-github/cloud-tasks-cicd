"""Shared fixtures: in-memory AWS mock with moto (no network)."""

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.aws import dynamodb_client, s3_client, sqs_client
from app.config import get_settings
from app.main import app


@pytest.fixture
def aws_mock():
    """Spin up in-memory DynamoDB/S3/SQS with moto and create the resources the app expects."""
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
    """FastAPI `TestClient` running against the moto mocks."""
    return TestClient(app)
