"""S3 access for task attachments (see wiki: task, naming-recursos)."""

from app.aws import s3_client
from app.config import get_settings


def upload_attachment(key: str, content: bytes) -> None:
    s3_client().put_object(Bucket=get_settings().attachments_bucket, Key=key, Body=content)
