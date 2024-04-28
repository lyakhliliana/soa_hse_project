from sqlalchemy import Column, String, Integer

from common.base_orm_model import BaseOrmModel


class LikeDao(BaseOrmModel):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(String(20), nullable=False)
    post_id = Column(Integer, nullable=False)


class ViewDao(BaseOrmModel):
    __tablename__ = 'view'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(String(20), nullable=False)
    post_id = Column(Integer, nullable=False)
