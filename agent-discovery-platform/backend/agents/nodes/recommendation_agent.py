from backend.agents.state import DiscoveryState
from backend.agents.routing import adaptive_router
import time
import logging

logger = logging.getLogger(__name__)

async def recommendation_agent(state: DiscoveryState) -> DiscoveryState:
    """Synthesizes search/ranking results into final recommendations."""
    start_time = time.time()
    ranked_agents = state.get("ranked_results", [])
    mcp_servers = state.get("mcp_candidates", [])
    
    model = await adaptive_router.select_model("recommendation_agent", state.get("intent", {}).get("complexity", "medium"), state.get("cost_budget_remaining", 0.05))
    logger.info(f"RecommendationAgent running with {model}")
    
    # Mock LLM Synthesis
    recommended_agents = ranked_agents[:3] # Top 3
    recommended_mcp = mcp_servers[:2]
    
    composition = "Use Customer Support Agent directly."
    if not recommended_agents and recommended_mcp:
        composition = "No exact agent found. Recommend composing a new agent using the Jira MCP Server tools."
        
    estimated_savings = {
        "development_hours_saved": 120 if recommended_agents else 40,
        "cost_saved_usd": 12000 if recommended_agents else 4000
    }
    
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "recommendation_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": model,
        "tokens": 150
    }
    
    return {
        "recommended_agents": recommended_agents,
        "recommended_mcp": recommended_mcp,
        "composition_strategy": composition,
        "estimated_savings": estimated_savings,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
