import os
from uuid import UUID

from fastapi import Depends, Header, HTTPException, APIRouter, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.kafka_managers.producer import send_message
from social_network_api.src.grpc_client.post.post_client_api import ContentGRPCClient
from social_network_api.src.grpc_client.statistics.statistics_client_api import StatisticsGRPCClient
from social_network_api.src.kafka.entities import kafka_producer_likes, kafka_producer_views
from social_network_api.src.models.dao import SessionDao, UserDao
from social_network_api.src.utils.session_maker import get_session

statistics_app = APIRouter(prefix="")
HOST_GRPC = os.getenv('HOST_GRPC', '192.168.1.65')
post_grpc_client = ContentGRPCClient(host=HOST_GRPC)
statistics_grpc_client = StatisticsGRPCClient(host=HOST_GRPC)


async def check_session_key(session: AsyncSession = Depends(get_session), session_key: UUID = Header(...)) -> UserDao:
    cur_session: SessionDao = (await session.execute(
        select(SessionDao).where(SessionDao.key == session_key))).unique().scalars().one_or_none()
    if not cur_session:
        raise HTTPException(status_code=401, detail=f'Действие недоступно.')
    cur_user: UserDao = (await session.execute(
        select(UserDao).where(UserDao.login == cur_session.login))).unique().scalars().one_or_none()
    if cur_user is None:
        raise HTTPException(status_code=401, detail=f'Логин не найде.')
    return cur_user


@statistics_app.post('/like', summary='Поставить лайк посту')
async def like_post(
    post_id: int,
    user: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.get_post(post_id=post_id))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')

    topic = os.getenv('TOPIC_NAME_LIKES')
    async with kafka_producer_likes.session() as session:
        await send_message(session, topic,
                           {'post_id': post_id, 'login': user.login, 'user_id': user.id,
                            "author_login": response.user_login})
    return Response(status_code=201, media_type='text/plain', content='Лайк поставлен.')


@statistics_app.post('/view', summary='Просмотреть пост')
async def view_post(
    post_id: int,
    user: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.get_post(post_id=post_id))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')

    topic = os.getenv('TOPIC_NAME_VIEWS')
    async with kafka_producer_views.session() as session:
        await send_message(session, topic, {'post_id': post_id, 'login': user.login, 'user_id': user.id,
                                            "author_login": response.user_login})
    return Response(status_code=201, media_type='text/plain', content='Просмотр отмечен.')


@statistics_app.get('/statistics/{post_id}', summary='Получить статистику поста')
async def get_post_stat(post_id: int):
    response = (await statistics_grpc_client.get_statistics(post_id=post_id))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return {'post_id': response.post_id, 'views': response.views, 'likes': response.likes}


@statistics_app.get('/top_posts', summary='Получить топ-5 постов по флагу view/like')
async def get_top_posts(flag: str):
    if flag not in ("view", "like"):
        raise HTTPException(status_code=400, detail='Flag is like or view')
    response = (await statistics_grpc_client.get_top_posts(flag=flag))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return [{'post_id': post.post_id, 'views': post.views, 'likes': post.likes, 'login': post.login} for post in
            response]


@statistics_app.get('/top_users', summary='Получить топ-3 пользователей')
async def get_top_users():
    response = (await statistics_grpc_client.get_top_users())
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return [{'login': post.login, 'likes': post.likes} for post in response]
