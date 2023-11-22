from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/test")
def read_test():
    return {"msg": "Hello World :3"}
