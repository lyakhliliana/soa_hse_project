# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: content.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcontent.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"8\n\x11\x43reatePostRequest\x12\x12\n\nuser_login\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"\x1d\n\x0f\x43hangePostReply\x12\n\n\x02id\x18\x01 \x01(\x03\"D\n\x11UpdatePostRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nuser_login\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"3\n\x11\x44\x65letePostRequest\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nuser_login\x18\x02 \x01(\t\"\x1c\n\x0eGetPostRequest\x12\n\n\x02id\x18\x01 \x01(\x03\"?\n\x0cGetPostReply\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x12\n\nuser_login\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"%\n\x0fGetPostsRequest\x12\x12\n\nuser_login\x18\x01 \x01(\t2\x89\x02\n\x07\x43ontent\x12\x34\n\nCreatePost\x12\x12.CreatePostRequest\x1a\x10.ChangePostReply\"\x00\x12\x34\n\nUpdatePost\x12\x12.UpdatePostRequest\x1a\x10.ChangePostReply\"\x00\x12\x34\n\nDeletePost\x12\x12.DeletePostRequest\x1a\x10.ChangePostReply\"\x00\x12+\n\x07GetPost\x12\x0f.GetPostRequest\x1a\r.GetPostReply\"\x00\x12/\n\x08GetPosts\x12\x10.GetPostsRequest\x1a\r.GetPostReply\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'content_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CREATEPOSTREQUEST']._serialized_start=50
  _globals['_CREATEPOSTREQUEST']._serialized_end=106
  _globals['_CHANGEPOSTREPLY']._serialized_start=108
  _globals['_CHANGEPOSTREPLY']._serialized_end=137
  _globals['_UPDATEPOSTREQUEST']._serialized_start=139
  _globals['_UPDATEPOSTREQUEST']._serialized_end=207
  _globals['_DELETEPOSTREQUEST']._serialized_start=209
  _globals['_DELETEPOSTREQUEST']._serialized_end=260
  _globals['_GETPOSTREQUEST']._serialized_start=262
  _globals['_GETPOSTREQUEST']._serialized_end=290
  _globals['_GETPOSTREPLY']._serialized_start=292
  _globals['_GETPOSTREPLY']._serialized_end=355
  _globals['_GETPOSTSREQUEST']._serialized_start=357
  _globals['_GETPOSTSREQUEST']._serialized_end=394
  _globals['_CONTENT']._serialized_start=397
  _globals['_CONTENT']._serialized_end=662
# @@protoc_insertion_point(module_scope)