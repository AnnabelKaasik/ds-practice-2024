# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_executor.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14order_executor.proto\x12\rorderexecutor\"*\n\x05Order\x12\x0f\n\x07orderId\x18\x01 \x01(\t\x12\x10\n\x08userName\x18\x02 \x01(\t\"!\n\x0e\x44\x65queueRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"P\n\x0f\x44\x65queueResponse\x12\x18\n\x10sending_an_order\x18\x01 \x01(\x08\x12#\n\x05order\x18\x02 \x01(\x0b\x32\x14.orderexecutor.Order\"B\n\x18\x41re_You_AvailableRequest\x12\x13\n\x0b\x65xecutor_id\x18\x01 \x01(\t\x12\x11\n\tleader_id\x18\x02 \x01(\t\"C\n\x19\x41re_You_AvailableResponse\x12\x13\n\x0b\x65xecutor_id\x18\x01 \x01(\t\x12\x11\n\tleader_id\x18\x02 \x01(\t2\xc8\x01\n\x14OrderExecutorService\x12H\n\x07\x44\x65queue\x12\x1d.orderexecutor.DequeueRequest\x1a\x1e.orderexecutor.DequeueResponse\x12\x66\n\x11\x41re_You_Available\x12\'.orderexecutor.Are_You_AvailableRequest\x1a(.orderexecutor.Are_You_AvailableResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_executor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=39
  _globals['_ORDER']._serialized_end=81
  _globals['_DEQUEUEREQUEST']._serialized_start=83
  _globals['_DEQUEUEREQUEST']._serialized_end=116
  _globals['_DEQUEUERESPONSE']._serialized_start=118
  _globals['_DEQUEUERESPONSE']._serialized_end=198
  _globals['_ARE_YOU_AVAILABLEREQUEST']._serialized_start=200
  _globals['_ARE_YOU_AVAILABLEREQUEST']._serialized_end=266
  _globals['_ARE_YOU_AVAILABLERESPONSE']._serialized_start=268
  _globals['_ARE_YOU_AVAILABLERESPONSE']._serialized_end=335
  _globals['_ORDEREXECUTORSERVICE']._serialized_start=338
  _globals['_ORDEREXECUTORSERVICE']._serialized_end=538
# @@protoc_insertion_point(module_scope)
