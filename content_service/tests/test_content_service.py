from pathlib import Path

import grpc
import httpx
import pytest
from testcontainers.compose import DockerCompose

import common.post_grpc.content_pb2 as content_pb2
import common.post_grpc.content_pb2_grpc as content_pb2_grpc


@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.fixture(scope='module')
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()


@pytest.fixture(scope='module')
def create_user():
    async def _impl():
        async with httpx.AsyncClient() as client:
            data = {
                'login': 'login',
                'password': 'password'
            }
            await client.post('http://0.0.0.0:30/user', json=data)

    return _impl


@pytest.mark.asyncio
async def test_get_post_by_id(docker_services, grpc_channel, create_user):
    await create_user()
    stub = content_pb2_grpc.ContentStub(grpc_channel)
    request = content_pb2.CreatePostRequest(user_login='login', content='some-content')
    response = stub.CreatePost(request)
    assert {'id': response.id} == {'id': 1}
