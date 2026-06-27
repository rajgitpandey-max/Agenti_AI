from backend.agents.state import DiscoveryState
from backend.search.ranking_engine import ranking_engine
import time
import logging

logger = logging.getLogger(__name__)

async def ranking_agent(state: DiscoveryState) -> DiscoveryState:
    """Applies the 8-Factor weighted ranking model to agent candidates."""
    start_time = time.time()
    candidates = state.get("agent_candidates", [])
    
    logger.info(f"RankingAgent ranking {len(candidates)} candidates")
    
    # query context used for capability matching
    query_context = {
        "capabilities": state.get("capabilities", []),
        "intent": state.get("intent", {})
    }
    
    ranked_results = ranking_engine.rank_candidates(query_context, candidates)
    
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "ranking_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": "N/A (Ranking Engine)",
        "tokens": 0
    }
    
    return {
        "ranked_results": ranked_results,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
