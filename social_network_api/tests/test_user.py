from pathlib import Path

import httpx
import pytest
from testcontainers.compose import DockerCompose


# TODO: we should run only grpc server
@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.mark.asyncio
async def test_create_user(docker_services):
    async with httpx.AsyncClient() as client:
        data = {
            'login': 'login',
            'password': 'password'
        }
        response = await client.post("http://0.0.0.0:30/user", json=data)
        assert response.status_code == 201
        assert response.text == 'Регистрация успешна!'


@pytest.mark.asyncio
async def test_create_user_and_auth(docker_services):
    async with httpx.AsyncClient() as client:
        data = {
            'login': 'login',
            'password': 'password'
        }
        await client.post("http://0.0.0.0:30/user", json=data)
        response = await client.post("http://0.0.0.0:30/user_authentication", json=data)
        assert response.status_code == 200
