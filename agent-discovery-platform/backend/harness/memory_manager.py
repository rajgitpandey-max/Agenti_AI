from backend.agents.state import DiscoveryState
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    """Handles short-term (session) and long-term (user) memory retrieval."""
    
    def get_session_context(self, user_id: str, tenant_id: str) -> dict:
        # Mock Redis/DB fetch for recent queries
        return {"recent_queries": ["looking for hr bot", "need jira access"]}
        
    def get_user_preferences(self, user_id: str) -> dict:
        # Mock long term preferences
        return {"preferred_environment": "aws", "role": "developer"}
        
    def enrich_query(self, query: str, context: dict, preferences: dict) -> str:
        # Basic prompt engineering to inject context
        role = preferences.get("role", "user")
        enriched = f"[Context: Role={role}] {query}"
        return enriched

memory_manager = MemoryManager()

async def memory_manager_node(state: DiscoveryState) -> DiscoveryState:
    user_id = state.get("user_id", "anonymous")
    tenant_id = state.get("tenant_id", "default")
    query = state.get("sanitized_query", state["user_query"])
    
    context = memory_manager.get_session_context(user_id, tenant_id)
    prefs = memory_manager.get_user_preferences(user_id)
    
    enriched = memory_manager.enrich_query(query, context, prefs)
    
    return {
        "session_context": context,
        "user_preferences": prefs,
        "enriched_query": enriched
    }
