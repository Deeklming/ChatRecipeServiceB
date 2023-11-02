from pydantic import BaseModel
from datetime import datetime
from models.users import Users
from models.posts import Posts
# from sqlmodel import JSON, SQLModel, Field, Column

class Comments(BaseModel):
    id: int
    post_id: Posts
    author: Users
    comment_id: int|None = None
    content: str
    like_cnt: int = 0
    created_at: datetime = datetime.datetime.now().isoformat(timespec="iso8601")
    public: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "post_id": "post",
                "author": "user",
                "comment_id": "comment",
                "content": "content",
                "like_cnt": 0,
                "created_at": "2023-11-02T13:30:00+09:00",
                "public": True
            }
        }
