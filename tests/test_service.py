from pathlib import Path

import httpx
import pytest
from uuid import UUID

from testcontainers.compose import DockerCompose


@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.mark.asyncio
async def test_create_and_auth_user(docker_services):
    async with httpx.AsyncClient() as client:
        data = {
            'login': 'login',
            'password': 'password'
        }
        response = await client.post("http://0.0.0.0:30/user", json=data)
        assert response.status_code == 201
        assert response.text == 'Регистрация успешна!'

        response = await client.post("http://0.0.0.0:30/user_authentication", json=data)
        assert response.status_code == 200
        session: str = response.json()['key']
        assert isinstance(UUID(session), UUID)


@pytest.mark.asyncio
async def test_create_post_and_like(docker_services):
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
        response = await client.post(
            'http://0.0.0.0:30/post', json=data, headers=headers
        )
        assert response.json() == {'id': 1}
        response = await client.get('http://0.0.0.0:30/post/1')
        assert response.status_code == 200
        assert response.json() == {'id': 1, 'content': 'some-content', 'user_login': 'login'}
