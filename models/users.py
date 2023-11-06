from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone, timedelta
from uuid import UUID
from fastapi import Query


class User(BaseModel):
    id: UUID
    email: EmailStr
    pw: str
    nickname: str = Query(min_length=3, max_length=20)
    country: str
    follows: dict[str, int|str] = {"count": 0}
    likes: dict[str, int|str] = {"count": 0}
    hashtags: list[str]|None = None
    image: str|None = None
    body: str|None = None
    created_at: datetime = datetime.now(timezone.utc)+timedelta(hours=9)
    status: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "email@email.com",
                "password": "password",
                "nickname": "nickname",
                "image": "https://url",
                "body": "self introduction",
                "follows": {"count": 0, "key": "value"},
                "likes": {"count": 0, "key": "value"},
                "hashtags": ["tag"],
                "country": "i10n",
                "created_at": "2023-11-02T13:30:00+09:00", # iso8601
                "status": True
            }
        }

class SignIn(BaseModel):
    email: EmailStr
    pw: str
    nickname: str
    token: str|None = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@email.com",
                "pw": "password",
                "nickname": "nickname",
                "token": "token"
            }
        }
