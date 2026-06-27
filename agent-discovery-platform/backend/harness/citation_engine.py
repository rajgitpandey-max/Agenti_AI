from backend.agents.state import DiscoveryState
import logging

logger = logging.getLogger(__name__)

class CitationEngine:
    """Attaches provenance and evidence to recommended agents."""
    
    def extract_citations(self, recommended_agents: list, mcp_servers: list) -> list:
        citations = []
        # Mock citation generation based on recommendations
        for idx, agent in enumerate(recommended_agents):
            citations.append({
                "source_id": agent.get("id", f"agent-{idx}"),
                "source_type": "agent_registry",
                "name": agent.get("name", "Unknown"),
                "relevance_score": agent.get("composite_score", 0.0),
                "excerpt": f"Matched on capability: {agent.get('capabilities', [])}"
            })
        return citations

citation_engine = CitationEngine()

async def citation_engine_node(state: DiscoveryState) -> DiscoveryState:
    agents = state.get("recommended_agents", [])
    mcps = state.get("recommended_mcp", [])
    
    citations = citation_engine.extract_citations(agents, mcps)
    
    return {
        "citations": citations
    }
