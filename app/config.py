"""App configuration read from the environment (see wiki: config-por-entorno)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App environment variables. Sensible defaults for local dev (`*-local`)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aws_endpoint_url: str = ""
    aws_region: str = "us-east-1"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"

    tasks_table: str = "tasks-local"
    attachments_bucket: str = "attachments-local"
    events_queue: str = "task-events-local"

    log_level: str = "INFO"


def get_settings() -> Settings:
    """Return the settings read from the current environment."""
    return Settings()
