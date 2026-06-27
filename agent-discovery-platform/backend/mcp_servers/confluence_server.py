from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("confluence-enterprise", dependencies=["confluence"])

MOCK_PAGES = [
    {"id": "1001", "title": "AI Platform Architecture", "space": "ENG", "labels": ["architecture", "ai"]},
    {"id": "1002", "title": "Customer Support Agent ADR", "space": "ENG", "labels": ["adr", "agent"]},
]

@mcp.tool()
async def search_pages(query: str, space: str = "", labels: List[str] = None) -> List[Dict[str, Any]]:
    """Search for Confluence pages matching the query."""
    return [p for p in MOCK_PAGES if query.lower() in p["title"].lower()]

@mcp.tool()
async def get_page_content(page_id: str) -> str:
    """Get the markdown content of a Confluence page."""
    return f"# Page {page_id}\n\nThis is mock content for the page."

@mcp.tool()
async def get_page_metadata(page_id: str) -> Dict[str, Any]:
    """Get page metadata (author, labels, last modified)."""
    return {"author": "Jane Doe", "labels": ["ai", "architecture"], "last_modified": "2023-10-27T10:00:00Z"}

@mcp.tool()
async def search_adrs(query: str) -> List[Dict[str, Any]]:
    """Search specifically for Architecture Decision Records."""
    return [p for p in MOCK_PAGES if "adr" in p["labels"] and query.lower() in p["title"].lower()]

@mcp.tool()
async def search_runbooks(query: str) -> List[Dict[str, Any]]:
    """Search specifically for operational runbooks."""
    return []

if __name__ == "__main__":
    mcp.run()
