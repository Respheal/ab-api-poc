from celery import Celery

from app import get_settings

settings = get_settings()

celery = Celery(
    __name__,
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
