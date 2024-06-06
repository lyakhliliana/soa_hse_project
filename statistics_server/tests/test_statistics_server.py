from pathlib import Path

import grpc
import httpx
import pytest
from testcontainers.compose import DockerCompose

import common.stat_grpc.statistics_pb2 as statistics_pb2
import common.stat_grpc.statistics_pb2_grpc as statistics_pb2_grpc


# @pytest.fixture(scope='module')
# def grpc_server():
#     server_process = Process(target=serve)
#     server_process.start()
#     for _ in range(10):
#         try:
#             with grpc.insecure_channel('0.0.0.0:50052') as channel:
#                 grpc.channel_ready_future(channel).result(timeout=1)
#             break
#         except grpc.FutureTimeoutError:
#             time.sleep(1)
#     yield
#     server_process.terminate()
#     server_process.join()

# TODO: we should run only grpc server
@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.fixture(scope='module')
def grpc_channel():
    channel = grpc.insecure_channel('0.0.0.0:50052')
    yield channel
    channel.close()


@pytest.fixture(scope='module')
def create_post():
    async def _impl():
        async with httpx.AsyncClient() as client:
            data = {
                'login': 'login',
                'password': 'password'
            }
            await client.post('http://0.0.0.0:30/user', json=data)
            response = await client.post('http://0.0.0.0:30/user_authentication', json=data)
            session = response.json()['key']
            headers = {
                'session-key': session
            }
            data = {
                'content': 'some-content'
            }
            await client.post(
                'http://0.0.0.0:30/post', json=data, headers=headers
            )
            response = await client.get('http://0.0.0.0:30/post/1')
            assert response.json() == {'id': 1, 'content': 'some-content', 'user_login': 'login'}

    return _impl


@pytest.mark.asyncio
async def test_get_post_by_id(docker_services, grpc_channel, create_post):
    await create_post()
    stub = statistics_pb2_grpc.StatisticsStub(grpc_channel)
    request = statistics_pb2.GetStatisticsByIdRequest(post_id=1)
    response = stub.GetStatisticsById(request)
    assert {
               'post_id': response.post_id, 'views': response.views, 'likes': response.likes
           } == {
               'post_id': 1, 'views': 0, 'likes': 0
           }


# @pytest.mark.asyncio
# async def test_get_users(docker_services, grpc_channel, create_post):
#     await create_post()
#     stub = statistics_pb2_grpc.StatisticsStub(grpc_channel)
#     request = statistics_pb2.EmptyRequest()
#     response = (await stub.GetTopUsers(request))
#     assert [{'login': post.login, 'likes': post.likes} for post in response] == [{'login': 'login', 'likes': 0}]
