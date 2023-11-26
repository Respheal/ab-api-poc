from fastapi import FastAPI
from celery import Celery

app = FastAPI()


celery = Celery(
    __name__, broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


@app.get("/test")
def read_test() -> dict[str, str]:
    return {"msg": "Hello World :3"}


@celery.task
def divide(x: int, y: int) -> float:
    return float(x / y)
