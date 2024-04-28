from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BookRead(_message.Message):
    __slots__ = ("title",)
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class BookStock(_message.Message):
    __slots__ = ("title", "stock")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    title: str
    stock: int
    def __init__(self, title: _Optional[str] = ..., stock: _Optional[int] = ...) -> None: ...

class BookWrite(_message.Message):
    __slots__ = ("title", "newStock")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    NEWSTOCK_FIELD_NUMBER: _ClassVar[int]
    title: str
    newStock: int
    def __init__(self, title: _Optional[str] = ..., newStock: _Optional[int] = ...) -> None: ...

class UpdateAck(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
