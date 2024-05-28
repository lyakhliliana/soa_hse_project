from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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

class GetTopPostsReply(_message.Message):
    __slots__ = ("post_replies",)
    POST_REPLIES_FIELD_NUMBER: _ClassVar[int]
    post_replies: _containers.RepeatedCompositeFieldContainer[PostReply]
    def __init__(self, post_replies: _Optional[_Iterable[_Union[PostReply, _Mapping]]] = ...) -> None: ...

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

class GetTopUsersReply(_message.Message):
    __slots__ = ("user_replies",)
    USER_REPLIES_FIELD_NUMBER: _ClassVar[int]
    user_replies: _containers.RepeatedCompositeFieldContainer[UserReply]
    def __init__(self, user_replies: _Optional[_Iterable[_Union[UserReply, _Mapping]]] = ...) -> None: ...
