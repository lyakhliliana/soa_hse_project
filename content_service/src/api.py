import asyncio
import logging
from datetime import datetime

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

import grpc

from common.post_grpc.content_pb2_grpc import ContentServicer
from content_service.src.models.dao import PostDao
from content_service.src.utils.session_maker import async_session

from common.post_grpc.content_pb2 import ChangePostReply, GetPostReply
from common.post_grpc.content_pb2_grpc import add_ContentServicer_to_server


class ContentService(ContentServicer):

    async def CreatePost(self, request, context):
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session
                new_post: PostDao = PostDao(user_login=request.user_login, content=request.content,
                                            created_at=datetime.now())
                session.add(new_post)
                await session.commit()
                return ChangePostReply(id=new_post.id)

    async def UpdatePost(self, request, context):
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session
                current_post: PostDao = (
                    await session.execute(select(PostDao).where(PostDao.id == request.id))
                ).unique().scalars().one_or_none()
                if current_post is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('No post to update')
                    return ChangePostReply()
                if current_post.user_login != request.user_login:
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details('Permission denied')
                    return ChangePostReply()
                else:
                    current_post.content = request.content
                    await session.commit()
                    return ChangePostReply(id=current_post.id)

    async def DeletePost(self, request, context):
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session
                current_post: PostDao = (
                    await session.execute(select(PostDao).where(PostDao.id == request.id))
                ).unique().scalars().one_or_none()
                if not current_post:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('No post to delete')
                    return ChangePostReply()
                if current_post.user_login != request.user_login:
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details('Permission denied')
                    return ChangePostReply()
                else:
                    await session.delete(current_post)
                    await session.commit()
                    return ChangePostReply(id=current_post.id)

    async def GetPost(self, request, context):
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session
                current_post: PostDao = (
                    await session.execute(select(PostDao).where(PostDao.id == request.id))
                ).unique().scalars().one_or_none()
                if not current_post:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('No post')
                    return GetPostReply()
                else:
                    return GetPostReply(
                        id=current_post.id,
                        user_login=current_post.user_login,
                        content=current_post.content
                    )

    async def GetPosts(self, request, context):
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session
                current_posts: Sequence[PostDao] = (
                    await session.execute(select(PostDao).where(PostDao.user_login == request.user_login))
                ).scalars().all()
                if not current_posts:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details('No post')
                    yield GetPostReply()
                else:
                    for post in current_posts:
                        yield GetPostReply(
                            id=post.id,
                            content=post.content,
                            user_login=post.user_login
                        )


async def serve() -> None:
    server = grpc.aio.server()
    add_ContentServicer_to_server(ContentService(), server)
    listen_addr = '0.0.0.0:50051'
    server.add_insecure_port(listen_addr)
    logging.info('Starting server on %s', listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
