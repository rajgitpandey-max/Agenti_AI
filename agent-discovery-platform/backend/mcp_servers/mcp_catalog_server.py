from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("mcp-catalog", dependencies=[])

@mcp.tool()
async def search_mcp_servers(query: str, category: str = "") -> List[Dict[str, Any]]:
    """Search for MCP servers in the enterprise catalog."""
    return [{"id": "mcp-1", "name": "Jira MCP Server", "status": "ACTIVE"}]

@mcp.tool()
async def get_server_details(server_id: str) -> Dict[str, Any]:
    """Get full MCP server metadata."""
    return {"id": server_id, "name": "Jira MCP Server", "description": "Interact with Jira issues."}

@mcp.tool()
async def list_tools(server_id: str) -> List[Dict[str, Any]]:
    """List tools provided by an MCP server."""
    return [{"name": "create_issue", "description": "Create a Jira issue"}]

@mcp.tool()
async def list_resources(server_id: str) -> List[Dict[str, Any]]:
    """List resources provided by an MCP server."""
    return [{"name": "project_list", "uri_template": "jira://projects/{project_key}"}]

@mcp.tool()
async def get_server_health(server_id: str) -> Dict[str, Any]:
    """Get health status and metrics for an MCP server."""
    return {"status": "healthy", "uptime_days": 42}

@mcp.tool()
async def get_server_owner(server_id: str) -> Dict[str, Any]:
    """Get team ownership info for an MCP server."""
    return {"team": "Platform Tools", "slack_channel": "#platform-tools"}

if __name__ == "__main__":
    mcp.run()
