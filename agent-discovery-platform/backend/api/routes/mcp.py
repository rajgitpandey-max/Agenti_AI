from fastapi import APIRouter, Depends
from backend.api.deps import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.models.mcp import MCPServer

router = APIRouter()

@router.get("/")
async def list_mcp_servers(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(MCPServer))
    return result.scalars().all()

@router.get("/{server_id}")
async def get_mcp_server(server_id: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(MCPServer).where(MCPServer.id == server_id))
    return result.scalar_one_or_none()
