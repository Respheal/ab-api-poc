from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # Base
    debug: bool = False
    project_name: str = "project_name"
    version: str = "0.0.0"
    description: str = ""
    environment: str = ""
    backend_cors_origins: list[AnyHttpUrl] = ["http://localhost:3000"]

    # Database
    postgres_host: str | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    # Celery

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
