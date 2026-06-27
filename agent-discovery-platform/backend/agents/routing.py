import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AdaptiveModelRouter:
    """Routes to optimal model based on cost, latency, quality."""

    def __init__(self):
        self.model_registry = {
            "gpt-4o-mini": {"cost_per_1k": 0.15, "avg_latency_ms": 400, "quality": 0.85},
            "gpt-4o":      {"cost_per_1k": 2.50, "avg_latency_ms": 800, "quality": 0.95},
        }
        self.cost_budget_per_query = 0.05  # $0.05 max per query

    async def select_model(self, agent_name: str, complexity: str, budget_remaining: float) -> str:
        """Select model considering: complexity, remaining budget, latency SLA."""
        logger.info(f"Selecting model for {agent_name} with complexity {complexity}, budget ${budget_remaining}")
        
        # Simple heuristics for MVP
        if complexity == "simple":
            return "gpt-4o-mini"
        elif complexity == "medium":
            # If budget is tight, fallback to mini
            if budget_remaining < 0.01:
                return "gpt-4o-mini"
            return "gpt-4o"
        else: # complex
            return "gpt-4o"

    async def track_cost(self, trace_id: str, model: str, tokens_used: int):
        """Record cost for budget tracking and analytics."""
        cost_info = self.model_registry.get(model, {"cost_per_1k": 0.0})
        cost = (tokens_used / 1000.0) * cost_info["cost_per_1k"]
        logger.debug(f"Trace {trace_id}: {model} used {tokens_used} tokens. Cost: ${cost:.5f}")
        return cost

    async def get_fallback_chain(self, primary_model: str) -> List[str]:
        """Return fallback models if primary fails."""
        if primary_model == "gpt-4o":
            return ["gpt-4o-mini"]
        return []

adaptive_router = AdaptiveModelRouter()
