import logging

import grpc
from common.stat_grpc.statistics_pb2 import (
    GetStatisticsByIdRequest,
    GetTopPostsRequest,
    EmptyRequest
)
from common.stat_grpc.statistics_pb2_grpc import StatisticsStub

_LOGGER = logging.getLogger(__name__)


class StatisticsGRPCClient:

    def __init__(self, host='localhost', port=50052):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = StatisticsStub(self.channel)

    async def get_statistics(self, post_id: int):
        request = GetStatisticsByIdRequest(post_id=post_id)
        try:
            response = self.stub.GetStatisticsById(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def get_top_posts(self, flag: str):
        request = GetTopPostsRequest(flag=flag)
        try:
            response = self.stub.GetTopPosts(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)

    async def get_top_users(self):
        request = EmptyRequest()
        try:
            response = self.stub.GetTopUsers(request)
            return response
        except grpc.RpcError as rpc_error:
            _LOGGER.error("Call failure: %s", rpc_error)
