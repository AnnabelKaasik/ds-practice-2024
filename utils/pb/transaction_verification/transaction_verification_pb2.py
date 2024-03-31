# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\x0cverification\"p\n\x0bVectorClock\x12\x33\n\x05\x63lock\x18\x01 \x03(\x0b\x32$.verification.VectorClock.ClockEntry\x1a,\n\nClockEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"A\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"(\n\x04Item\x12\x0e\n\x06\x62ookid\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"\xa8\x01\n\x0bTransaction\x12!\n\x05items\x18\x01 \x03(\x0b\x32\x12.verification.Item\x12 \n\x04user\x18\x02 \x01(\x0b\x32\x12.verification.User\x12-\n\x0b\x63redit_card\x18\x03 \x01(\x0b\x32\x18.verification.CreditCard\x12%\n\x1dterms_and_conditions_accepted\x18\x04 \x01(\x08\"{\n\x18VerifyTransactionRequest\x12.\n\x0btransaction\x18\x01 \x01(\x0b\x32\x19.verification.Transaction\x12/\n\x0cvector_clock\x18\x02 \x01(\x0b\x32\x19.verification.VectorClock\"u\n\x19VerifyTransactionResponse\x12\x10\n\x08is_valid\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12/\n\x0cvector_clock\x18\x03 \x01(\x0b\x32\x19.verification.VectorClock2\x86\x01\n\x1eTransactionVerificationService\x12\x64\n\x11VerifyTransaction\x12&.verification.VerifyTransactionRequest\x1a\'.verification.VerifyTransactionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VECTORCLOCK_CLOCKENTRY']._options = None
  _globals['_VECTORCLOCK_CLOCKENTRY']._serialized_options = b'8\001'
  _globals['_VECTORCLOCK']._serialized_start=48
  _globals['_VECTORCLOCK']._serialized_end=160
  _globals['_VECTORCLOCK_CLOCKENTRY']._serialized_start=116
  _globals['_VECTORCLOCK_CLOCKENTRY']._serialized_end=160
  _globals['_USER']._serialized_start=162
  _globals['_USER']._serialized_end=199
  _globals['_CREDITCARD']._serialized_start=201
  _globals['_CREDITCARD']._serialized_end=266
  _globals['_ITEM']._serialized_start=268
  _globals['_ITEM']._serialized_end=308
  _globals['_TRANSACTION']._serialized_start=311
  _globals['_TRANSACTION']._serialized_end=479
  _globals['_VERIFYTRANSACTIONREQUEST']._serialized_start=481
  _globals['_VERIFYTRANSACTIONREQUEST']._serialized_end=604
  _globals['_VERIFYTRANSACTIONRESPONSE']._serialized_start=606
  _globals['_VERIFYTRANSACTIONRESPONSE']._serialized_end=723
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_start=726
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_end=860
# @@protoc_insertion_point(module_scope)
