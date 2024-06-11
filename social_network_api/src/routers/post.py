import os
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from social_network_api.src.models.dao import UserDao, SessionDao
from social_network_api.src.models.dto import PostCreate, PostUpdate
from social_network_api.src.utils.session_maker import get_session
from social_network_api.src.grpc_client.post.post_client_api import ContentGRPCClient

from uuid import UUID

post_app = APIRouter(prefix="/post")
HOST_GRPC = os.getenv('HOST_GRPC', '192.168.1.65')
post_grpc_client = ContentGRPCClient(host=HOST_GRPC)


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


@post_app.post('', summary='Создание поста')
async def create_post(
        post_to_post: PostCreate,
        user: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.create_post(user_login=user.login, content=post_to_post.content))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return {'id': response.id}


@post_app.put('', summary='Обновление контента поста')
async def update_post(
        post_to_update: PostUpdate,
        user: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.update_post(
        user_login=user.login,
        content=post_to_update.content,
        post_id=post_to_update.id
    ))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return {'id': response.id}


@post_app.delete('/{post_id}', summary='Удаление поста')
async def delete_post(
        post_id: int,
        user: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.delete_post(post_id=post_id, user_login=user.login))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return {'id': response.id}


@post_app.get('/{post_id}', summary='Получить пост')
async def get_post(
        post_id: int,
        _: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.get_post(post_id=post_id))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return {'id': response.id, 'content': response.content, 'user_login': response.user_login}


@post_app.get('s/{user_login}', summary='Получить все посты по конкретному логину')
async def get_posts(
        user_login: str,
        _: UserDao = Depends(check_session_key)
):
    response = (await post_grpc_client.get_posts(user_login=user_login))
    if not response:
        raise HTTPException(status_code=401, detail='GRPC client error')
    return [{'id': post.id, 'content': post.content, 'user_login': post.user_login} for post in response]
