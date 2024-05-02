from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentRequest(_message.Message):
    __slots__ = ("orderId", "amount", "currency")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    amount: float
    currency: str
    def __init__(self, orderId: _Optional[str] = ..., amount: _Optional[float] = ..., currency: _Optional[str] = ...) -> None: ...

class PaymentResponse(_message.Message):
    __slots__ = ("orderId", "success", "message")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    success: bool
    message: str
    def __init__(self, orderId: _Optional[str] = ..., success: bool = ..., message: _Optional[str] = ...) -> None: ...
