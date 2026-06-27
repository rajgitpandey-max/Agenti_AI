from mcp.server.fastmcp import FastMCP
import asyncio
from typing import List, Dict, Any

# Create the GitHub MCP server
mcp = FastMCP("github-enterprise", dependencies=["github"])

# Mock data
MOCK_REPOS = [
    {"owner": "enterprise", "repo": "customer-support-agent", "topics": ["ai", "langchain", "customer-support"]},
    {"owner": "enterprise", "repo": "hr-policy-agent", "topics": ["ai", "llama_index", "hr"]},
    {"owner": "enterprise", "repo": "doc-summarizer", "topics": ["ai", "nlp"]},
]

@mcp.tool()
async def search_repositories(query: str, org: str = "enterprise", language: str = "python") -> List[Dict[str, Any]]:
    """Search for repositories matching the query in the organization."""
    return [r for r in MOCK_REPOS if query.lower() in r["repo"].lower() or any(query.lower() in t for t in r["topics"])]

@mcp.tool()
async def search_code(query: str, language: str = "python", path: str = "") -> List[Dict[str, Any]]:
    """Search for code snippets matching the query."""
    return [{"repo": "enterprise/customer-support-agent", "file": "agent.py", "snippet": "def handle_customer_query(query):\n    pass"}]

@mcp.tool()
async def get_readme(owner: str, repo: str) -> str:
    """Get the markdown content of a repository's README.md."""
    return f"# {repo}\n\nThis is a mock README for {owner}/{repo}.\n\nIt is an AI agent that does things."

@mcp.tool()
async def get_repo_metadata(owner: str, repo: str) -> Dict[str, Any]:
    """Get repository metadata (stars, forks, topics)."""
    return {"stars": 42, "forks": 12, "topics": ["ai", "agent"]}

@mcp.tool()
async def list_workflows(owner: str, repo: str) -> List[Dict[str, Any]]:
    """List GitHub Actions workflows for a repository."""
    return [{"name": "CI", "state": "active", "path": ".github/workflows/ci.yml"}]

@mcp.tool()
async def search_agent_definitions(query: str) -> List[Dict[str, Any]]:
    """Search for agent manifest YAML files in repositories."""
    return [{"repo": "enterprise/customer-support-agent", "file": "agent.yaml", "content": "name: Customer Support\nversion: 1.0.0"}]

if __name__ == "__main__":
    mcp.run()
