import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from testcontainers.compose import DockerCompose


@pytest_asyncio.fixture(scope='module')
async def kafka_services():
    doker_compose_file = Path(__file__).parent.parent / 'tools' / 'kafka-dev'
    with DockerCompose(doker_compose_file, compose_file_name='docker-compose-test.yml') as docker_services:
        await asyncio.sleep(10)
        yield docker_services


@pytest_asyncio.fixture(scope='module')
async def extra_consumer(kafka_services):
    bootstrap_servers = 'localhost:9092'
    consumer = AIOKafkaConsumer(
        'views',
        bootstrap_servers=bootstrap_servers,
        group_id='test_group',
        value_deserializer=lambda v: v.decode('utf-8')
    )
    await consumer.start()
    await consumer.stop()


@pytest.mark.asyncio
async def test_kafka_produce_consume(extra_consumer):
    bootstrap_servers = 'localhost:9092'
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: v.encode('utf-8')
    )
    await producer.start()

    consumer = AIOKafkaConsumer(
        'views',
        bootstrap_servers=bootstrap_servers,
        group_id='test_group',
        value_deserializer=lambda v: v.decode('utf-8')
    )
    await consumer.start()

    try:
        await producer.send_and_wait('views', 'test_message')
    finally:
        await producer.stop()
    await asyncio.sleep(5)

    try:
        messages = []
        async for msg in consumer:
            messages.append(msg.value)
            if len(messages) >= 1:
                break
        assert messages == ['test_message']
    finally:
        await consumer.stop()
