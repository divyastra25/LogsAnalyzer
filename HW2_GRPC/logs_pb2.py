# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: logs.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nlogs.proto\x12\x04logs\";\n\rGetMessageReq\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\r\n\x05start\x18\x02 \x01(\t\x12\r\n\x05\x64\x65lta\x18\x03 \x01(\t\"4\n\rMessagesReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x12\n\ncoded_logs\x18\x02 \x03(\t2I\n\x0cLogRetriever\x12\x39\n\x0bGetMessages\x12\x13.logs.GetMessageReq\x1a\x13.logs.MessagesReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'logs_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETMESSAGEREQ._serialized_start=20
  _GETMESSAGEREQ._serialized_end=79
  _MESSAGESREPLY._serialized_start=81
  _MESSAGESREPLY._serialized_end=133
  _LOGRETRIEVER._serialized_start=135
  _LOGRETRIEVER._serialized_end=208
# @@protoc_insertion_point(module_scope)
