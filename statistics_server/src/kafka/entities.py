import asyncio
import os

from common.kafka_managers.consumer import KafkaConsumer

kafka = os.getenv('KAFKA_INSTANCE')
CONFIG = {'bootstrap_servers': kafka}

kafka_consumer_likes = KafkaConsumer(CONFIG)
kafka_consumer_views = KafkaConsumer(CONFIG)
