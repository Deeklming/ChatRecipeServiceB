from pydantic import BaseModel
# from sqlmodel import JSON, SQLModel, Field, Column

class Tags(BaseModel):
    id: int
    tag: str
    note: str|None = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "tag": "tag",
                "note": "note, #colorcode"
            }
        }
