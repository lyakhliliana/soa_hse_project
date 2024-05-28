import asyncio
import logging
import os

import grpc

from common.stat_grpc.statistics_pb2_grpc import add_StatisticsServicer_to_server
from statistics_server.src.grpc_service import StatisticsService
from statistics_server.src.kafka.callback_functions import likes_callback, views_callback
from statistics_server.src.kafka.entities import kafka_consumer_likes, kafka_consumer_views, event_loop


async def serve() -> None:
    server = grpc.aio.server()
    add_StatisticsServicer_to_server(StatisticsService(), server)
    listen_addr = '0.0.0.0:50052'
    server.add_insecure_port(listen_addr)
    logging.info('Starting server on %s', listen_addr)
    await server.start()
    await server.wait_for_termination()


async def lifespan():
    topic = os.getenv('TOPIC_NAME_LIKES')
    await kafka_consumer_likes.init_consumer(topic, likes_callback)
    event_loop.create_task(kafka_consumer_likes.consume())

    topic = os.getenv('TOPIC_NAME_VIEWS')
    await kafka_consumer_views.init_consumer(topic, views_callback)
    event_loop.create_task(kafka_consumer_views.consume())

    try:
        await serve()
    finally:
        await kafka_consumer_likes.stop()
        await kafka_consumer_views.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(lifespan())
