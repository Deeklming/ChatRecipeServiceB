from fastapi import FastAPI
from todo import todo_router

app = FastAPI()

@app.get("/")
async def hi() -> dict:
    return {
        "message": "Hi2"
    }

app.include_router(todo_router)
