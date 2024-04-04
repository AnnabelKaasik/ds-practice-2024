from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Order(_message.Message):
    __slots__ = ("orderId", "userName")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    userName: str
    def __init__(self, orderId: _Optional[str] = ..., userName: _Optional[str] = ...) -> None: ...

class DequeueRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DequeueResponse(_message.Message):
    __slots__ = ("sending_an_order", "order")
    SENDING_AN_ORDER_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    sending_an_order: bool
    order: Order
    def __init__(self, sending_an_order: bool = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class Are_You_AvailableRequest(_message.Message):
    __slots__ = ("request_from_id", "leader_id", "request_to_id")
    REQUEST_FROM_ID_FIELD_NUMBER: _ClassVar[int]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TO_ID_FIELD_NUMBER: _ClassVar[int]
    request_from_id: str
    leader_id: str
    request_to_id: str
    def __init__(self, request_from_id: _Optional[str] = ..., leader_id: _Optional[str] = ..., request_to_id: _Optional[str] = ...) -> None: ...

class Are_You_AvailableResponse(_message.Message):
    __slots__ = ("executor_id", "leader_id", "available")
    EXECUTOR_ID_FIELD_NUMBER: _ClassVar[int]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    executor_id: str
    leader_id: str
    available: bool
    def __init__(self, executor_id: _Optional[str] = ..., leader_id: _Optional[str] = ..., available: bool = ...) -> None: ...
