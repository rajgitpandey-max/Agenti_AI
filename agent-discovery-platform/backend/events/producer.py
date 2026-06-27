from aiokafka import AIOKafkaProducer
from backend.config import settings
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class EventProducer:
    def __init__(self):
        self.producer = None
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        
    async def connect(self):
        if not self.producer:
            logger.info("Connecting to Kafka Producer...")
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            logger.info("Kafka Producer started.")
            
    async def disconnect(self):
        if self.producer:
            await self.producer.stop()
            self.producer = None
            logger.info("Kafka Producer stopped.")
            
    async def publish(self, topic: str, event_data: dict):
        if not self.producer:
            await self.connect()
        try:
            await self.producer.send_and_wait(topic, event_data)
            logger.debug(f"Published event to {topic}")
        except Exception as e:
            logger.error(f"Failed to publish event to {topic}: {e}")

event_producer = EventProducer()
