from typing import Any

from fastapi import FastAPI

from app import get_settings
from app.db.models import HealthCheck
from app.routers import users, comic

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
)

app.include_router(users.router)
app.include_router(comic.router)


@app.get("/", response_model=HealthCheck, tags=["status"])
def health_check() -> dict[str, Any]:
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
