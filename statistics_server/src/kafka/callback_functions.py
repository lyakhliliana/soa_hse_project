import json

from fastapi import HTTPException
from sqlalchemy import select

from statistics_server.src.models.dao import LikeDao, ViewDao
from statistics_server.src.models.dto import LikeDto, ViewDto
from statistics_server.src.utils.session_maker import async_session



async def likes_callback(msg):
    request_info = LikeDto(**json.loads(msg.value.decode('ascii')))
    async with async_session() as session:
        async with session.begin():
            f = (LikeDao.user_id == request_info.user_id) & (LikeDao.post_id == request_info.post_id)
            like: LikeDao = (await session.execute(select(LikeDao).where(f))).unique().scalars().one_or_none()
            if like:
                raise HTTPException(status_code=409, detail=f'Лайк уже существует.')

            new_like: LikeDao = LikeDao(login=request_info.login, post_id=request_info.post_id,
                                        user_id=request_info.user_id, author_login=request_info.author_login)
            session.add(new_like)
            await session.commit()



async def views_callback(msg):
    request_info = ViewDto(**json.loads(msg.value.decode('ascii')))
    async with async_session() as session:
        async with session.begin():
            f = (ViewDao.user_id == request_info.user_id) & (ViewDao.post_id == request_info.post_id)
            view: ViewDao = (await session.execute(select(ViewDao).where(f))).unique().scalars().one_or_none()
            if view:
                raise HTTPException(status_code=409, detail=f'Просмотр уже существует.')

            new_view: ViewDao = ViewDao(login=request_info.login, post_id=request_info.post_id,
                                        user_id=request_info.user_id, author_login=request_info.author_login)
            session.add(new_view)
            await session.commit()
