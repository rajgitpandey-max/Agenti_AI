from fastapi import APIRouter, Depends
from typing import List
from backend.api.deps import get_current_user, get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.models.agent import Agent

router = APIRouter()

@router.get("/")
async def list_agents(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Agent))
    agents = result.scalars().all()
    return agents

@router.get("/{agent_id}")
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    return result.scalar_one_or_none()
