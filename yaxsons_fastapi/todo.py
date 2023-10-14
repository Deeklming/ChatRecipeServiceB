from fastapi import APIRouter
from model import Todo

todo_router = APIRouter()

todo_list = []

@todo_router.get("/todo")
async def todos() -> dict:
    return {
        "todos": todo_list
    }

@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "todo added successfully."
    }
