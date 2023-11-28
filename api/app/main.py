from typing import Any, Generator

from contextlib import asynccontextmanager

from fastapi import FastAPI
from celery import Celery

from app import settings
from app.db.session import create_db_and_tables
from app.db.models import HealthCheck
from app.routers import users, recipes


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    # Create database for local development and testing
    if settings.environment != "production":
        create_db_and_tables()
    yield


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
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
