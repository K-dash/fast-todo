from fastapi import FastAPI

from fast_todo.routers import auth, users
from fast_todo.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Hello World!"}
