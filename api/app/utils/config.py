from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    debug: bool = False
    project_name: str = "project_name"
    version: str = "0.0.0"
    description: str = ""
    environment: str = ""

    # Database
    postgres_host: str | None = None
    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    # Celery

    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
