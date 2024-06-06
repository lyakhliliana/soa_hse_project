# import asyncio
# import os
# from pathlib import Path
#
# import pytest
# import pytest_asyncio
# from testcontainers.compose import DockerCompose
#
# from common.kafka_managers.producer import KafkaProducerSession, send_message
# from common.kafka_managers.consumer import KafkaConsumer
#
#
# @pytest.fixture(scope='module')
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest_asyncio.fixture(scope='module')
# async def kafka_services():
#     doker_compose_file = Path(__file__).parent.parent / 'tools' / 'kafka-dev'
#     with DockerCompose(doker_compose_file, compose_file_name='docker-compose-test.yml') as docker_services:
#         os.environ['KAFKA_INSTANCE'] = 'kafka:29092'
#         await asyncio.sleep(20)
#         yield docker_services
#         os.environ.pop('KAFKA_INSTANCE')
#
#
# def callback(msg):
#     assert msg.value.decode('ascii') == {'post_id': 1, 'login': 'login', 'user_id': 1, 'author_login': 'login'}
#
#
# @pytest_asyncio.fixture(scope='module')
# async def kafka_producer(kafka_services):
#     kafka = os.getenv('KAFKA_INSTANCE')
#     config = {'bootstrap_servers': kafka}
#     kafka_producer = KafkaProducerSession(config)
#     await kafka_producer.init_producer()
#     yield kafka_producer
#     await kafka_producer.stop()
#
#
# @pytest_asyncio.fixture(scope='module')
# async def kafka_consumer(kafka_services):
#     kafka = os.getenv('KAFKA_INSTANCE')
#     config = {'bootstrap_servers': kafka}
#     kafka_consumer = KafkaConsumer(config)
#     await kafka_consumer.init_consumer('topic', callback)
#     await kafka_consumer.consume()
#     yield kafka_consumer
#     await kafka_consumer.stop()
#
#
# @pytest.mark.asyncio
# async def test_kafka_produce_consume(kafka_producer, kafka_consumer):
#     async with kafka_producer.session() as producer:
#         await send_message(
#             producer,
#             'likes',
#             {'post_id': 1, 'login': 'login', 'user_id': 1, 'author_login': 'login'}
#         )
