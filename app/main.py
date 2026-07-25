"""Entry point of the API microservice (see wiki: microservicio-api)."""

from fastapi import FastAPI

from app.api import health, tasks

app = FastAPI(title="Cloud Tasks API")

app.include_router(health.router)
app.include_router(tasks.router)
