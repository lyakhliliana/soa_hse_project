from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from datetime import date


class RegisterData(BaseModel):
    login: str
    password: str


class UserInfo(RegisterData):
    id: int
    name: str
    surname: str
    birthdate: date
    mail: str
    number_phone: str


class SessionKey(BaseModel):
    key: UUID


class UserUpdate(BaseModel):
    login: str
    name: Optional[str] = None
    surname: Optional[str] = None
    birthdate: Optional[date] = None
    mail: Optional[str] = None
    number_phone: Optional[str] = None


class PostCreate(BaseModel):
    user_login: str
    content: str


class PostUpdate(PostCreate):
    id: UUID


class PostDelete(BaseModel):
    id: UUID
    user_login: str


class PostGet(BaseModel):
    id: UUID
    user_login: str


class PostsGet(BaseModel):
    id: UUID
    user_login: str
    user_with_posts_login: str


class PostCreate(BaseModel):
    content: str


class PostUpdate(BaseModel):
    id: int
    content: str
