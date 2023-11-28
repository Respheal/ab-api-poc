from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    debug: bool = False
    project_name: str
    version: str
    description: str
    environment: str

    # Database
    postgres_host: str | None
    postgres_db: str | None
    postgres_user: str | None
    postgres_password: str | None

    # Celery

    celery_broker_url: str | None
    celery_result_backend: str | None
