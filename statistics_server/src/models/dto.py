from pydantic import BaseModel


class LikeDto(BaseModel):
    user_id: int
    login: str
    author_login: str
    post_id: int


class ViewDto(BaseModel):
    user_id: int
    login: str
    author_login: str
    post_id: int
