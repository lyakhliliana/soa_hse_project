from contextlib import asynccontextmanager

from fastapi import FastAPI

from social_network_api.src.kafka.entities import kafka_producer_likes, kafka_producer_views
from social_network_api.src.routers.post import post_app
from social_network_api.src.routers.statistics import statistics_app
from social_network_api.src.routers.user import user_app


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await kafka_producer_likes.init_producer()
    await kafka_producer_views.init_producer()
    yield
    await kafka_producer_likes.stop()
    await kafka_producer_views.stop()


app = FastAPI(title='Social Network API', lifespan=lifespan)
app.include_router(post_app)
app.include_router(statistics_app)
app.include_router(user_app)
