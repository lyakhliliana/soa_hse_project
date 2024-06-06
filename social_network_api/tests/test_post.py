from pathlib import Path

import httpx
import pytest
from testcontainers.compose import DockerCompose


@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.fixture(scope='module')
def create_user():
    async def _impl():
        async with httpx.AsyncClient() as client:
            data = {
                'login': 'login',
                'password': 'password'
            }
            await client.post('http://0.0.0.0:30/user', json=data)
            response = (await client.post("http://0.0.0.0:30/user_authentication", json=data))
            return response.json()['key']

    return _impl


@pytest.mark.asyncio
async def test_create_post(docker_services, create_user):
    session = (await create_user())
    async with httpx.AsyncClient() as client:
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


@pytest.mark.asyncio
async def test_get_posts(docker_services):
    async with httpx.AsyncClient() as client:
        response = await client.get('http://0.0.0.0:30/posts/login')
        assert response.status_code == 200
        assert response.json() == [{'id': 1, 'content': 'some-content', 'user_login': 'login'}]
