from typing import Any


from fastapi import FastAPI
from celery import Celery

from app import get_settings
from app.db.models import HealthCheck
from app.routers import users, recipes

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
)

celery = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check() -> dict[str, Any]:
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
