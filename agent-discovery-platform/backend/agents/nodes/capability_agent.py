from backend.agents.state import DiscoveryState
from backend.agents.routing import adaptive_router
import time
import logging

logger = logging.getLogger(__name__)

async def capability_agent(state: DiscoveryState) -> DiscoveryState:
    """Extracts required capabilities and formulates search queries."""
    start_time = time.time()
    intent = state.get("intent", {})
    query = state.get("sanitized_query", state["user_query"])
    
    model = await adaptive_router.select_model("capability_agent", intent.get("complexity", "medium"), state.get("cost_budget_remaining", 0.05))
    logger.info(f"CapabilityAgent running with model {model}")
    
    # Mock LLM capability extraction
    capabilities = ["text_summarization", "query_routing"] if "support" in query.lower() else ["data_analysis"]
    
    search_queries = {
        "registry": f"Find agents with capabilities: {', '.join(capabilities)}",
        "github": query,
        "confluence": query,
        "mcp_catalog": f"Tools for {intent.get('domain', 'general')}"
    }
    
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "capability_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": model,
        "tokens": 75
    }
    
    return {
        "capabilities": capabilities,
        "search_queries": search_queries,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
