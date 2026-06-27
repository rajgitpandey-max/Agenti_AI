from aiokafka import AIOKafkaConsumer
from backend.config import settings
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class EventConsumer:
    def __init__(self, topics: list, group_id: str = "agent-discovery-group"):
        self.topics = topics
        self.group_id = group_id
        self.consumer = None
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        
    async def connect(self):
        if not self.consumer:
            logger.info(f"Connecting Kafka Consumer to topics: {self.topics}...")
            self.consumer = AIOKafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            await self.consumer.start()
            logger.info("Kafka Consumer started.")
            
    async def disconnect(self):
        if self.consumer:
            await self.consumer.stop()
            self.consumer = None
            logger.info("Kafka Consumer stopped.")
            
    async def consume(self):
        if not self.consumer:
            await self.connect()
        
        try:
            async for msg in self.consumer:
                topic = msg.topic
                data = msg.value
                logger.info(f"Received event on {topic}: {data}")
                await self.process_event(topic, data)
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled")
            
    async def process_event(self, topic: str, data: dict):
        # Dispatch event processing
        if topic == "discovery.feedback":
            logger.info("Processing feedback event...")
        elif topic == "discovery.guardrail":
            logger.info("Processing guardrail violation event...")
        else:
            pass

# To run the consumer in the background
async def start_consumer_loop():
    topics = ["discovery.feedback", "discovery.guardrail", "agent.lifecycle"]
    consumer = EventConsumer(topics)
    await consumer.consume()
