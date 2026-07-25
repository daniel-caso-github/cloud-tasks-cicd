"""Single factory for boto3 clients (see wiki: config-endpoint-aws).

No boto3 client is created outside this module. If `AWS_ENDPOINT_URL` is set
(e.g. pointing to LocalStack), clients use that endpoint; if empty, they point to real AWS.
"""

from typing import Any

import boto3

from app.config import get_settings


def _client(service: str) -> Any:
    settings = get_settings()
    kwargs: dict[str, Any] = {
        "region_name": settings.aws_region,
        "aws_access_key_id": settings.aws_access_key_id,
        "aws_secret_access_key": settings.aws_secret_access_key,
    }
    if settings.aws_endpoint_url:
        kwargs["endpoint_url"] = settings.aws_endpoint_url
    return boto3.client(service, **kwargs)


def dynamodb_client() -> Any:
    return _client("dynamodb")


def s3_client() -> Any:
    return _client("s3")


def sqs_client() -> Any:
    return _client("sqs")
