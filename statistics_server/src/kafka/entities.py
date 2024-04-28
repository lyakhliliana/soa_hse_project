import asyncio
import os

from common.kafka_managers.consumer import KafkaConsumer

event_loop = asyncio.get_event_loop()
kafka = os.getenv('KAFKA_INSTANCE')
CONFIG = {'bootstrap_servers': kafka, 'loop': event_loop}

kafka_consumer_likes = KafkaConsumer(CONFIG)
kafka_consumer_views = KafkaConsumer(CONFIG)
