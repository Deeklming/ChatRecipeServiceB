from pydantic import BaseModel
from datetime import datetime
from models.users import Users
from models.tags import Tags
# from sqlmodel import JSON, SQLModel, Field, Column

class Posts(BaseModel):
    id: int
    author: Users
    title: str
    content: str
    image: str|None = None
    view_cnt: int = 0
    like_cnt: int = 0
    hashtags: list[Tags]|None = None
    updated_at: datetime = datetime.datetime.now().isoformat(timespec="iso8601")
    created_at: datetime = datetime.datetime.now().isoformat(timespec="iso8601")
    public: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "author": "user",
                "title": "title",
                "content": "content",
                "image": "https://url",
                "view_cnt": 0,
                "like_cnt": 0,
                "hashtags": ["tag"],
                "updated_at": "2023-11-02T13:30:00+09:00",
                "created_at": "2023-11-02T13:30:00+09:00",
                "public": True
            }
        }
