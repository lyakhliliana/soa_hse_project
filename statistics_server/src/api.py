import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response


from statistics_server.src.kafka.callback_functions import likes_callback, views_callback
from statistics_server.src.kafka.entities import kafka_consumer_likes, kafka_consumer_views, event_loop
from statistics_server.src.models.dto import LikeDto


@asynccontextmanager
async def lifespan(_app: FastAPI):
    topic = os.getenv('TOPIC_NAME_LIKES')
    await kafka_consumer_likes.init_consumer(topic, likes_callback)
    event_loop.create_task(kafka_consumer_likes.consume())

    topic = os.getenv('TOPIC_NAME_VIEWS')
    await kafka_consumer_views.init_consumer(topic, views_callback)
    event_loop.create_task(kafka_consumer_views.consume())

    yield
    await kafka_consumer_likes.stop()
    await kafka_consumer_views.stop()


app = FastAPI(title='Statistic API', lifespan=lifespan)


@app.post('/joke',
          summary='Method with response 200.')
async def score_agreement(_: LikeDto):
    return Response(status_code=200, media_type='text/plain', content='Stub')
