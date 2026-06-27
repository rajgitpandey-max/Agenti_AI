import operator
from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage

class DiscoveryState(TypedDict):
    # Input
    user_query: str
    user_id: str
    tenant_id: str
    filters: Dict[str, Any]

    # Harness: Guardrails
    input_guardrail_result: Dict[str, Any]     # {safe, violations, sanitized_query}
    sanitized_query: str             # Query after PII/injection removal

    # Harness: Memory
    session_context: Dict[str, Any]            # Recent queries, selected agents
    user_preferences: Dict[str, Any]           # Learned preferences from history
    enriched_query: str              # Query + user context

    # Harness: Model Routing
    model_tier: str                  # simple | medium | complex
    model_used: str                  # actual model selected
    cost_budget_remaining: float     # per-query cost budget

    # Intent Agent
    intent: Dict[str, Any]                     # use_case, domain, confidence, complexity

    # Capability Agent
    capabilities: List[str]
    search_queries: Dict[str, Any]             # per-source optimized queries

    # Search Agent
    agent_candidates: List[Dict[str, Any]]
    mcp_candidates: List[Dict[str, Any]]
    github_results: List[Dict[str, Any]]
    confluence_results: List[Dict[str, Any]]

    # Ranking Agent
    ranked_results: List[Dict[str, Any]]

    # Recommendation Agent
    recommended_agents: List[Dict[str, Any]]
    recommended_mcp: List[Dict[str, Any]]
    composition_strategy: str
    estimated_savings: Dict[str, Any]

    # Governance Agent
    governance_status: List[Dict[str, Any]]

    # Evaluation Agent (LLM-as-Judge)
    quality_score: float
    evaluation_rubric: Dict[str, Any]          # {relevance, coverage, diversity, actionability}
    evaluation_notes: str

    # Harness: Citations
    citations: List[Dict[str, Any]]            # {source, url, relevance, excerpt}

    # Harness: Confidence
    confidence_scores: Dict[str, Any]          # {overall, intent, search_coverage, ranking}

    # Harness: Response Validation
    validation_result: Dict[str, Any]          # {valid, issues[]}
    output_guardrail_result: Dict[str, Any]    # {safe, violations}

    # Metadata
    messages: Annotated[List[BaseMessage], operator.add]
    workflow_steps: List[Dict[str, Any]]
    trace_id: str
    errors: List[str]
