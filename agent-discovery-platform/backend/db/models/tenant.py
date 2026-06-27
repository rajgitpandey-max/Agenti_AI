from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from backend.db.database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    
    teams = relationship("Team", back_populates="tenant")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    slack_channel = Column(String, nullable=True)
    email = Column(String, nullable=True)
    lead_name = Column(String, nullable=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    tenant = relationship("Tenant", back_populates="teams")
    agents = relationship("Agent", back_populates="team")
    mcp_servers = relationship("MCPServer", back_populates="team")
