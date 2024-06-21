from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from common.stat_grpc.statistics_pb2 import GetStatisticsByIdReply, GetStatisticsByIdRequest, GetTopPostsRequest, \
    EmptyRequest, PostReply, UserReply
from common.stat_grpc.statistics_pb2_grpc import StatisticsServicer
from statistics_server.src.models.dao import LikeDao, ViewDao
from statistics_server.src.utils.session_maker import async_session


class StatisticsService(StatisticsServicer):

    async def GetStatisticsById(self, request: GetStatisticsByIdRequest, context) -> GetStatisticsByIdReply:
        """Получение статистики поста по id"""
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session

                cnt_func = func.count(LikeDao.user_id.distinct()).label("likes")
                query = select(cnt_func).group_by(LikeDao.post_id).where(LikeDao.post_id == request.post_id)
                likes = (await session.execute(query)).scalar()

                cnt_func = func.count(ViewDao.user_id.distinct()).label("views")
                query = select(cnt_func).group_by(ViewDao.post_id).where(ViewDao.post_id == request.post_id)
                views = (await session.execute(query)).scalar()

                return GetStatisticsByIdReply(post_id=request.post_id, likes=likes, views=views)

    async def GetTopPosts(self, request: GetTopPostsRequest, context):
        """"Получение топ-5 постов по просмотрам или лайкам"""
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session

                database = LikeDao if request.flag == "like" else ViewDao
                cnt_func = func.count(database.user_id.distinct()).label("amount")
                query = select(database.post_id, database.author_login, cnt_func).group_by(
                    database.post_id, database.author_login).order_by(desc(cnt_func)).limit(5)
                top_posts = (await session.execute(query)).all()

        for post in top_posts:
            post_dict = post._asdict()
            yield PostReply(post_id=post_dict["post_id"], login=post_dict["author_login"], amount=post_dict["amount"])

    async def GetTopUsers(self, request: EmptyRequest, context):
        """"Получение топ-3 пользователей по лайкам"""
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession = session

                cnt_func = func.count(LikeDao.user_id).label("likes")
                query = select(LikeDao.author_login, cnt_func).group_by(
                    LikeDao.author_login).order_by(desc(cnt_func)).limit(3)
                top_users = (await session.execute(query)).all()

        for user in top_users:
            user_dict = user._asdict()
            yield UserReply(login=user_dict["author_login"], likes=user_dict["likes"])
