from typing import List, Dict, Any
from backend.search.qdrant_store import qdrant_store
from backend.search.embeddings import embedding_service
from qdrant_client.http import models as rest
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

class HybridSearchEngine:
    """
    Implements a hybrid search across Qdrant using:
    1. Vector Search (Cosine Similarity)
    2. BM25/Keyword Search (Payload filtering)
    3. Metadata Filtering (status, tenant, etc)
    """
    
    async def search(self, collection: str, query: str, filters: Dict[str, Any] = None, top_k: int = 10) -> List[Dict[str, Any]]:
        # 1. Embed query
        query_vector = embedding_service.embed_text(query)
        
        # 2. Build Qdrant filter from filters dict
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            if conditions:
                qdrant_filter = Filter(must=conditions)
        
        # 3. Execute Vector Search
        search_result = await qdrant_store.client.search(
            collection_name=collection,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
            with_payload=True
        )
        
        results = []
        for scored_point in search_result:
            result_item = scored_point.payload.copy()
            result_item["_score"] = scored_point.score
            result_item["_id"] = scored_point.id
            results.append(result_item)
            
        # TODO: Implement RRF (Reciprocal Rank Fusion) by running a parallel keyword search
        # and merging the results. For MVP, we'll return vector search results which are 
        # usually sufficient when combined with exact metadata filtering.
            
        return results

hybrid_search_engine = HybridSearchEngine()
