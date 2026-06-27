from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import Optional
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self):
        self._driver: Optional[AsyncDriver] = None

    async def connect(self):
        if not self._driver:
            logger.info("Connecting to Neo4j...")
            self._driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD.get_secret_value())
            )
            await self._driver.verify_connectivity()
            logger.info("Connected to Neo4j.")

    async def close(self):
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("Closed Neo4j connection.")

    async def execute_query(self, query: str, parameters: dict = None):
        if not self._driver:
            await self.connect()
        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            return [record.data() async for record in result]

neo4j_client = Neo4jClient()
