from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("agent-registry", dependencies=[])

@mcp.tool()
async def search_agents(query: str, category: str = "", status: str = "") -> List[Dict[str, Any]]:
    """Search for agents in the enterprise registry."""
    return [{"id": "agent-1", "name": "Customer Support Agent", "status": "PRODUCTION", "category": "Support"}]

@mcp.tool()
async def get_agent_details(agent_id: str) -> Dict[str, Any]:
    """Get full agent manifest from the registry."""
    return {"id": agent_id, "name": "Customer Support Agent", "description": "Handles customer queries", "tech_stack": ["python", "langchain"]}

@mcp.tool()
async def get_agent_versions(agent_id: str) -> List[Dict[str, Any]]:
    """Get version history for an agent."""
    return [{"version": "1.0.0", "channel": "stable"}, {"version": "1.1.0-beta", "channel": "experimental"}]

@mcp.tool()
async def get_agent_owner(agent_id: str) -> Dict[str, Any]:
    """Get team and contact info for an agent's owner."""
    return {"team": "Support Tech", "slack_channel": "#support-tech", "lead": "Alice"}

@mcp.tool()
async def get_agent_dependencies(agent_id: str) -> List[Dict[str, Any]]:
    """Get dependency tree for an agent."""
    return [{"type": "model", "ref": "gpt-4o"}]

@mcp.tool()
async def list_capabilities(domain: str = "") -> List[str]:
    """List available capabilities in the taxonomy."""
    return ["text_summarization", "query_routing", "data_extraction"]

if __name__ == "__main__":
    mcp.run()
