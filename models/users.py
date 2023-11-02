from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.tags import Tags
from models.posts import Posts
from models.comments import Comments
# from sqlmodel import JSON, SQLModel, Field, Column

class Users(BaseModel):
    id: int
    email: EmailStr
    password: str
    nickname: str = email.split('@')[0]
    image: str|None = None
    body: str|None = None
    follows: dict[str, int|str]
    likes: dict[str, int|Posts|Comments]
    hashtags: list[Tags]|None = None
    country: str
    created_at: datetime = datetime.datetime.now().isoformat(timespec="iso8601")
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
    password: str
    token: str|None = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "email@email.com",
                "password": "password",
                "token": "token"
            }
        }


# class User(SQLModel, table=True):
#     email: EmailStr = Field(primary_key=True)
#     password: str
#     username: str
#     events: Optional[List[Event]] = Field(sa_column=Column(JSON))
