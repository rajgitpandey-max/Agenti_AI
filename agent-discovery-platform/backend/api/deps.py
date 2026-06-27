from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session

async def get_current_user():
    # Mock authentication dependency
    return {"id": "user-123", "tenant_id": "tenant-abc", "role": "developer"}
