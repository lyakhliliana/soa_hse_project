import logging

import grpc
from common.post_grpc.content_pb2 import (
    CreatePostRequest,
    UpdatePostRequest,
    DeletePostRequest,
    GetPostRequest,
    GetPostsRequest
)
from common.post_grpc.content_pb2_grpc import ContentStub

_LOGGER = logging.getLogger(__name__)


class ContentGRPCClient:

    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = ContentStub(self.channel)

    async def create_post(self, user_login: str, content: str):
        request = CreatePostRequest(user_login=user_login, content=content)
        try:
            response = self.stub.CreatePost(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def update_post(self, user_login: str, post_id: int, content: str):
        request = UpdatePostRequest(user_login=user_login, id=post_id, content=content)
        try:
            response = self.stub.UpdatePost(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def delete_post(self, user_login: str, post_id: int):
        request = DeletePostRequest(user_login=user_login, id=post_id)
        try:
            response = self.stub.DeletePost(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def get_post(self, post_id: int):
        request = GetPostRequest(id=post_id)
        try:
            response = self.stub.GetPost(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def get_posts(self, user_login: str):
        request = GetPostsRequest(user_login=user_login)
        try:
            response = self.stub.GetPosts(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)
