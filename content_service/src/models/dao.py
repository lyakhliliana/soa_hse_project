from sqlalchemy import Column, String, DateTime, Integer

from common.base_orm_model import BaseOrmModel


class PostDao(BaseOrmModel):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_login = Column(String(20), nullable=False)