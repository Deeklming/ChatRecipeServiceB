from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []

@todo_router.get("/todo", response_model=TodoItems) #response_model 반환 형식 모델로 설정
async def todos() -> dict:
    return {
        "todos": todo_list
    }

@todo_router.post("/todo", status_code=201)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "todo added successfully."
    }

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The ID of the todo to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "todo with supplied ID doesn't exist.",
    )

@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="The ID of the todo to be updated.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "todo updated successfully."
            }
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "todo with supplied ID doesn't exist.",
    )

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int = Path(..., title="The ID of the todo to be deleted.")) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "todo deleted successfully."
            }
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "todo with supplied ID doesn't exist.",
    )

@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "all todo deleted successfully."
    }
