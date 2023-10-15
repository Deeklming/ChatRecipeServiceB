from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    item: str
    status: str

class Todo(BaseModel):
    id: int
    item: Item

    class Config:
        json_schema_extra = {
            "example": {
                "id": 10,
                "item": {
                    "item": "Nested models10",
                    "status": "completed10"
                }
            }
        }

class TodoItem(BaseModel):
    item: Item

    class Config:
        json_schema_extra = {
            "example": {
                "item": {
                    "item": "Nested models update",
                    "status": "completed update"
                }
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        json_schema_extra = {
            "example": {
                "todos":[
                    {
                        "item": "Nested models 21",
                        "status": "completed 21"
                    },
                    {
                        "item": "Nested models 22",
                        "status": "completed 22"
                    }
                ]
            }
        }