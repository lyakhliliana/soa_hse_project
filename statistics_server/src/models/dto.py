from pydantic import BaseModel


class LikeDto(BaseModel):
    login: str
    post_id: int


class ViewDto(BaseModel):
    login: str
    post_id: int
