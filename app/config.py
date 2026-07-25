"""Configuración de la app leída desde el entorno (ver wiki: config-por-entorno)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables de entorno de la app. Defaults sensatos para dev local (`*-local`)."""

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
    """Devuelve las settings leyendo el entorno actual."""
    return Settings()
