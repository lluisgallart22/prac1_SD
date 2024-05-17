from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageRequest(_message.Message):
    __slots__ = ("sender", "receiver", "text")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    receiver: str
    text: str
    def __init__(self, sender: _Optional[str] = ..., receiver: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class MessageResponse(_message.Message):
    __slots__ = ("sender", "text")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    sender: str
    text: str
    def __init__(self, sender: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...
