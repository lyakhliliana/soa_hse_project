from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.dialects import postgresql

from common.base_orm_model import BaseOrmModel


class UserDao(BaseOrmModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String(20),nullable=False)
    password = Column(String(20), nullable=False)
    name = Column(String(30), nullable=True)
    surname = Column(String(30), nullable=True)
    birthdate = Column(Date, nullable=True)
    mail = Column(String(30), nullable=True)
    mobile_phone_no = Column(String(30), nullable=True)


class SessionDao(BaseOrmModel):
    __tablename__ = 'session'
    login = Column(String(20), primary_key=True, nullable=False)
    key = Column(postgresql.UUID(as_uuid=True), nullable=False)
