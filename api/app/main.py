from fastapi import FastAPI

from app.db.session import create_db_and_tables
from app.routers import users, recipes


app = FastAPI()

app.include_router(users.router)
app.include_router(recipes.router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


@app.get("/test")
def read_test() -> dict[str, str]:
    return {"msg": "Hello World :3"}
