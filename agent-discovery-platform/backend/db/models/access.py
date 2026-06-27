import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.db.database import Base

class AccessRequest(Base):
    __tablename__ = "access_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    resource_type = Column(String, nullable=False) # agent|mcp_server
    resource_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False, default="pending") # pending|approved|rejected
    justification = Column(Text, nullable=True)
    approver_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
