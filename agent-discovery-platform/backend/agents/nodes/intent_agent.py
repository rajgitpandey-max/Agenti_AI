from backend.agents.state import DiscoveryState
from backend.agents.routing import adaptive_router
import time
import logging

logger = logging.getLogger(__name__)

async def intent_agent(state: DiscoveryState) -> DiscoveryState:
    """Extracts intent, domain, and complexity from the query."""
    start_time = time.time()
    query = state.get("enriched_query", state.get("sanitized_query", state["user_query"]))
    
    # 1. Determine complexity (simple heuristic for MVP)
    complexity = "simple"
    if len(query.split()) > 15 or "vs" in query or "compare" in query:
        complexity = "complex"
    elif len(query.split()) > 7:
        complexity = "medium"
        
    # 2. Select model
    budget = state.get("cost_budget_remaining", 0.05)
    model = await adaptive_router.select_model("intent_agent", complexity, budget)
    
    # 3. Simulate LLM Call (In production, use LangChain LLM with structured output)
    logger.info(f"IntentAgent analyzing query: '{query}' using {model}")
    
    intent_data = {
        "use_case": "customer_support" if "support" in query.lower() else "general",
        "domain": "support" if "support" in query.lower() else "engineering",
        "confidence": 0.9,
        "complexity": complexity
    }
    
    # Record step
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "intent_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": model,
        "tokens": 50
    }
    
    return {
        "intent": intent_data,
        "model_tier": complexity,
        "model_used": model,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
