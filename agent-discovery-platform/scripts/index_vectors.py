import asyncio
import logging
from backend.search.qdrant_store import qdrant_store
from backend.search.indexer import indexer_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing Qdrant collections...")
    await qdrant_store.initialize_collections()
    
    # Mock data to index
    mock_agents = [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "name": "Customer Support Agent",
            "description": "Handles tier 1 customer support queries using historical tickets and product documentation.",
            "category": "Support",
            "status": "PRODUCTION",
            "capabilities": ["text_summarization", "query_routing"],
            "team_id": "team-support"
        },
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "name": "HR Policy Assistant",
            "description": "Answers employee questions about company policies, benefits, and time off.",
            "category": "HR",
            "status": "PRODUCTION",
            "capabilities": ["q_and_a", "document_retrieval"],
            "team_id": "team-hr"
        }
    ]
    
    logger.info("Indexing mock agents...")
    await indexer_service.index_batch("agents", mock_agents)
    
    logger.info("Indexing complete.")

if __name__ == "__main__":
    asyncio.run(main())
