import os
from uuid import UUID

from fastapi import Depends, Header, HTTPException, APIRouter, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.kafka_managers.producer import send_message
from social_network_api.src.kafka.entities import kafka_producer_likes, kafka_producer_views
from social_network_api.src.models.dao import SessionDao, UserDao
from social_network_api.src.utils.session_maker import get_session

statistics_app = APIRouter(prefix="")


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
    topic = os.getenv('TOPIC_NAME_LIKES')
    async with kafka_producer_likes.session() as session:
        await send_message(session, topic, {'post_id': post_id, 'login': user.login})
    return Response(status_code=201, media_type='text/plain', content='Лайк поставлен.')


@statistics_app.post('/view', summary='Просмотреть пост')
async def view_post(
    post_id: int,
    user: UserDao = Depends(check_session_key)
):
    topic = os.getenv('TOPIC_NAME_VIEWS')
    async with kafka_producer_views.session() as session:
        await send_message(session, topic, {'post_id': post_id, 'login': user.login})
    return Response(status_code=201, media_type='text/plain', content='Просмотр отмечен.')
