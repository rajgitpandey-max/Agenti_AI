from backend.agents.state import DiscoveryState
from backend.agents.routing import adaptive_router
import time
import logging

logger = logging.getLogger(__name__)

async def evaluation_agent(state: DiscoveryState) -> DiscoveryState:
    """LLM-as-a-Judge: Evaluates the final recommendation quality."""
    start_time = time.time()
    
    # Usually evaluate with a cheaper/faster model or a specific evaluator model
    model = await adaptive_router.select_model("evaluation_agent", "simple", state.get("cost_budget_remaining", 0.05))
    logger.info(f"EvaluationAgent (LLM-as-Judge) running with {model}")
    
    # Mock LLM evaluation
    rubric = {
        "relevance": 0.9,
        "coverage": 0.8,
        "diversity": 0.7,
        "actionability": 0.95
    }
    quality_score = sum(rubric.values()) / len(rubric)
    
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "evaluation_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": model,
        "tokens": 100
    }
    
    return {
        "quality_score": quality_score,
        "evaluation_rubric": rubric,
        "evaluation_notes": "The recommendations highly align with the user intent.",
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
