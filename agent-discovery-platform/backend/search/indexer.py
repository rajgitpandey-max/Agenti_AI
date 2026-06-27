import uuid
from typing import List, Dict, Any
from backend.search.qdrant_store import qdrant_store
from backend.search.embeddings import embedding_service
from qdrant_client.http import models as rest
import logging

logger = logging.getLogger(__name__)

class IndexerService:
    """Service to handle batch indexing of data into Qdrant."""
    
    async def index_batch(self, collection_name: str, items: List[Dict[str, Any]]):
        if not items:
            return
            
        logger.info(f"Indexing {len(items)} items into {collection_name}...")
        
        # Extract text to embed (combine name and description)
        texts_to_embed = [
            f"{item.get('name', '')}. {item.get('description', '')}"
            for item in items
        ]
        
        # Generate embeddings in batch
        vectors = embedding_service.embed_batch(texts_to_embed)
        
        # Prepare Qdrant points
        points = []
        for i, item in enumerate(items):
            # Use provided ID if available (and is valid UUID format), else generate
            point_id = item.get("id")
            try:
                if point_id:
                    uuid.UUID(str(point_id))
                else:
                    point_id = str(uuid.uuid4())
            except ValueError:
                point_id = str(uuid.uuid4())
                
            points.append(
                rest.PointStruct(
                    id=point_id,
                    vector=vectors[i],
                    payload=item
                )
            )
            
        # Upsert to Qdrant
        await qdrant_store.client.upsert(
            collection_name=collection_name,
            points=points
        )
        logger.info(f"Successfully indexed batch into {collection_name}.")

indexer_service = IndexerService()
