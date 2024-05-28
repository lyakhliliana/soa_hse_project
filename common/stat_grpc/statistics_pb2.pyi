from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetStatisticsByIdRequest(_message.Message):
    __slots__ = ("post_id",)
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class GetStatisticsByIdReply(_message.Message):
    __slots__ = ("post_id", "likes", "views")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    VIEWS_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    likes: int
    views: int
    def __init__(self, post_id: _Optional[int] = ..., likes: _Optional[int] = ..., views: _Optional[int] = ...) -> None: ...

class GetTopPostsRequest(_message.Message):
    __slots__ = ("flag",)
    FLAG_FIELD_NUMBER: _ClassVar[int]
    flag: str
    def __init__(self, flag: _Optional[str] = ...) -> None: ...

class PostReply(_message.Message):
    __slots__ = ("post_id", "login", "amount")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    login: str
    amount: int
    def __init__(self, post_id: _Optional[int] = ..., login: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class EmptyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UserReply(_message.Message):
    __slots__ = ("login", "likes")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    login: str
    likes: int
    def __init__(self, login: _Optional[str] = ..., likes: _Optional[int] = ...) -> None: ...
