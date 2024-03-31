from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreatePostRequest(_message.Message):
    __slots__ = ("user_login", "content")
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    user_login: str
    content: str
    def __init__(self, user_login: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class ChangePostReply(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UpdatePostRequest(_message.Message):
    __slots__ = ("id", "user_login", "content")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_login: str
    content: str
    def __init__(self, id: _Optional[int] = ..., user_login: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class DeletePostRequest(_message.Message):
    __slots__ = ("id", "user_login")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_login: str
    def __init__(self, id: _Optional[int] = ..., user_login: _Optional[str] = ...) -> None: ...

class GetPostRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetPostReply(_message.Message):
    __slots__ = ("id", "user_login", "content")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    id: int
    user_login: str
    content: str
    def __init__(self, id: _Optional[int] = ..., user_login: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class GetPostsRequest(_message.Message):
    __slots__ = ("user_login",)
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    user_login: str
    def __init__(self, user_login: _Optional[str] = ...) -> None: ...
