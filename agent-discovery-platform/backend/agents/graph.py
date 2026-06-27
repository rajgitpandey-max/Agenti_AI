from langgraph.graph import StateGraph, END
from backend.agents.state import DiscoveryState
from backend.agents.nodes.intent_agent import intent_agent
from backend.agents.nodes.capability_agent import capability_agent
from backend.agents.nodes.search_agent import search_agent
from backend.agents.nodes.ranking_agent import ranking_agent
from backend.agents.nodes.recommendation_agent import recommendation_agent
from backend.agents.nodes.governance_agent import governance_agent
from backend.agents.nodes.evaluation_agent import evaluation_agent

# Import real harness nodes
from backend.harness.guardrails import input_guardrail_node
from backend.harness.memory_manager import memory_manager_node
from backend.harness.citation_engine import citation_engine_node
from backend.harness.confidence_calibrator import confidence_calibrator_node
from backend.harness.response_validator import response_validator_node

# Build the 13-node Pipeline (7 Agents + 5 inline Harness nodes)
workflow = StateGraph(DiscoveryState)

# Add Harness Nodes
workflow.add_node("input_guardrail", input_guardrail_node)
workflow.add_node("memory_manager", memory_manager_node)
workflow.add_node("citation_engine", citation_engine_node)
workflow.add_node("confidence_calibrator", confidence_calibrator_node)
workflow.add_node("response_validator", response_validator_node)

# Add Agent Nodes
workflow.add_node("intent_agent", intent_agent)
workflow.add_node("capability_agent", capability_agent)
workflow.add_node("search_agent", search_agent)
workflow.add_node("ranking_agent", ranking_agent)
workflow.add_node("recommendation_agent", recommendation_agent)
workflow.add_node("governance_agent", governance_agent)
workflow.add_node("evaluation_agent", evaluation_agent)

# Define Edges (The Pipeline)
workflow.set_entry_point("input_guardrail")

workflow.add_edge("input_guardrail", "memory_manager")
workflow.add_edge("memory_manager", "intent_agent")
workflow.add_edge("intent_agent", "capability_agent")
workflow.add_edge("capability_agent", "search_agent")
workflow.add_edge("search_agent", "ranking_agent")
workflow.add_edge("ranking_agent", "recommendation_agent")

# Parallel split after recommendation
workflow.add_edge("recommendation_agent", "governance_agent")
workflow.add_edge("recommendation_agent", "evaluation_agent")
workflow.add_edge("recommendation_agent", "citation_engine")

# Join into confidence calibration and validation
workflow.add_edge("governance_agent", "confidence_calibrator")
workflow.add_edge("evaluation_agent", "confidence_calibrator")
workflow.add_edge("citation_engine", "confidence_calibrator")

workflow.add_edge("confidence_calibrator", "response_validator")
workflow.add_edge("response_validator", END)

# Compile graph
discovery_pipeline = workflow.compile()
