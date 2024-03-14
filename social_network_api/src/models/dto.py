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
