from backend.agents.state import DiscoveryState
from backend.search.hybrid_search import hybrid_search_engine
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def search_agent(state: DiscoveryState) -> DiscoveryState:
    """Orchestrates parallel search across Qdrant and MCP servers."""
    start_time = time.time()
    search_queries = state.get("search_queries", {})
    
    logger.info("SearchAgent starting parallel search...")
    
    # In a real implementation, this would call the MCP servers.
    # For MVP, we do hybrid search against Qdrant collections.
    
    async def search_registry():
        return await hybrid_search_engine.search("agents", search_queries.get("registry", ""), top_k=5)
        
    async def search_mcp():
        return await hybrid_search_engine.search("mcp_servers", search_queries.get("mcp_catalog", ""), top_k=3)
        
    async def search_github():
        return await hybrid_search_engine.search("repositories", search_queries.get("github", ""), top_k=3)
        
    async def search_confluence():
        return await hybrid_search_engine.search("documents", search_queries.get("confluence", ""), top_k=3)
        
    # Execute in parallel
    results = await asyncio.gather(
        search_registry(),
        search_mcp(),
        search_github(),
        search_confluence(),
        return_exceptions=True
    )
    
    # Handle exceptions gracefully
    registry_res = results[0] if not isinstance(results[0], Exception) else []
    mcp_res = results[1] if not isinstance(results[1], Exception) else []
    github_res = results[2] if not isinstance(results[2], Exception) else []
    confluence_res = results[3] if not isinstance(results[3], Exception) else []
    
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "search_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": "N/A (Search Engine)",
        "tokens": 0
    }
    
    return {
        "agent_candidates": registry_res,
        "mcp_candidates": mcp_res,
        "github_results": github_res,
        "confluence_results": confluence_res,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
