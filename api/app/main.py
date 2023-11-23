from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"msg": "Hello World"}


@app.get("/test")
def read_test() -> dict[str, str]:
    return {"msg": "Hello World :3"}
