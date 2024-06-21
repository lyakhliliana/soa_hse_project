from pathlib import Path

import httpx
import pytest
from testcontainers.compose import DockerCompose

HOST = 'localhost'


@pytest.fixture(scope='module')
def docker_services():
    doker_compose_file = Path(__file__).parent.parent.parent
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose.yml') as docker_services:
        yield docker_services


@pytest.fixture(scope='module')
def create_user_and_post():
    async def _impl():
        async with httpx.AsyncClient() as client:
            data = {
                'login': 'login',
                'password': 'password'
            }
            await client.post(f'http://{HOST}:30/user', json=data)
            response = (await client.post(f'http://{HOST}:30/user_authentication', json=data))
            session = response.json()['key']
            headers = {
                'session-key': session
            }
            data = {
                'content': 'some-content'
            }
            await client.post(
                f'http://{HOST}:30/post', json=data, headers=headers
            )

    return _impl


@pytest.mark.asyncio
async def test_get_stats_by_post_id(docker_services, create_user_and_post):
    await create_user_and_post()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'http://{HOST}:30/statistics/1'
        )
        assert response.status_code == 200
        assert response.json() == {'post_id': 1, 'views': 0, 'likes': 0}


# @pytest.mark.asyncio
# async def test_get_top_users(docker_services):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f'http://{HOST}:30/top_posts')
#         assert response.status_code == 200
#         assert response.json() == [{'post_id': 1, 'views': 0, 'likes': 0}]
