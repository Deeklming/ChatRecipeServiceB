from pydantic import BaseModel
# from sqlmodel import JSON, SQLModel, Field, Column

class Tags(BaseModel):
    id: int
    category: str
    tag: str
    note: str|None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "category": "category",
                "tag": "tag",
                "note": "note, #colorcode"
            }
        }
