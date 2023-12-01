from typing import Any

from app import get_settings
from app.db.models import HealthCheck
from app.routers import auth, comic, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    debug=settings.debug,
    openapi_url="/openapi.json",
)

# Set all CORS enabled origins
if settings.backend_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.backend_cors_origins
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(comic.router)


@app.get("/", response_model=HealthCheck, tags=["status"])
def health_check() -> dict[str, Any]:
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
