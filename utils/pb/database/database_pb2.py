# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: database.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x64\x61tabase.proto\x12\x06\x62ookdb\"\x19\n\x08\x42ookRead\x12\r\n\x05title\x18\x01 \x01(\t\")\n\tBookStock\x12\r\n\x05title\x18\x01 \x01(\t\x12\r\n\x05stock\x18\x02 \x01(\x05\",\n\tBookWrite\x12\r\n\x05title\x18\x01 \x01(\t\x12\x10\n\x08newStock\x18\x02 \x01(\x05\"-\n\tUpdateAck\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xd4\x01\n\x0c\x42ookDatabase\x12+\n\x04Read\x12\x10.bookdb.BookRead\x1a\x11.bookdb.BookStock\x12-\n\x05Write\x12\x11.bookdb.BookWrite\x1a\x11.bookdb.UpdateAck\x12\x33\n\x0b\x63heck_Write\x12\x11.bookdb.BookWrite\x1a\x11.bookdb.UpdateAck\x12\x33\n\x0bUpdateSlave\x12\x11.bookdb.BookWrite\x1a\x11.bookdb.UpdateAckb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'database_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BOOKREAD']._serialized_start=26
  _globals['_BOOKREAD']._serialized_end=51
  _globals['_BOOKSTOCK']._serialized_start=53
  _globals['_BOOKSTOCK']._serialized_end=94
  _globals['_BOOKWRITE']._serialized_start=96
  _globals['_BOOKWRITE']._serialized_end=140
  _globals['_UPDATEACK']._serialized_start=142
  _globals['_UPDATEACK']._serialized_end=187
  _globals['_BOOKDATABASE']._serialized_start=190
  _globals['_BOOKDATABASE']._serialized_end=402
# @@protoc_insertion_point(module_scope)
