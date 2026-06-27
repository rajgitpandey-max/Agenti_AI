from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as rest
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

# Qdrant Collections
COLLECTIONS = ["agents", "mcp_servers", "repositories", "documents", "workflows", "tools"]
VECTOR_DIMENSION = 384 # all-MiniLM-L6-v2 dimension

class QdrantStore:
    def __init__(self):
        self.client = AsyncQdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            api_key=settings.QDRANT_API_KEY.get_secret_value() if settings.QDRANT_API_KEY else None
        )

    async def initialize_collections(self):
        for collection_name in COLLECTIONS:
            if not await self.client.collection_exists(collection_name):
                logger.info(f"Creating Qdrant collection: {collection_name}")
                await self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=rest.VectorParams(
                        size=VECTOR_DIMENSION,
                        distance=rest.Distance.COSINE
                    )
                )
                
                # Create payload index for BM25 hybrid search fallback
                await self.client.create_payload_index(
                    collection_name=collection_name,
                    field_name="name",
                    field_schema=rest.TextIndexParams(
                        type="text",
                        tokenizer=rest.TokenizerType.WORD,
                        min_token_len=2,
                        max_token_len=15,
                        lowercase=True
                    )
                )
                await self.client.create_payload_index(
                    collection_name=collection_name,
                    field_name="description",
                    field_schema=rest.TextIndexParams(
                        type="text",
                        tokenizer=rest.TokenizerType.WORD,
                        min_token_len=2,
                        max_token_len=15,
                        lowercase=True
                    )
                )
                logger.info(f"Collection {collection_name} created with indexes.")

qdrant_store = QdrantStore()
