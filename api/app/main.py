from fastapi import FastAPI
from celery import Celery

from app.db.session import create_db_and_tables
from app.routers import users, recipes


app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


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
