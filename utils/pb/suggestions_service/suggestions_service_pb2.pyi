from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Book(_message.Message):
    __slots__ = ("bookid", "title", "author")
    BOOKID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    bookid: str
    title: str
    author: str
    def __init__(self, bookid: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class getSuggestionsRequest(_message.Message):
    __slots__ = ("bookid",)
    BOOKID_FIELD_NUMBER: _ClassVar[int]
    bookid: str
    def __init__(self, bookid: _Optional[str] = ...) -> None: ...

class SuggestionsResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, items: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...
