import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.db.database import Base

class MCPServer(Base):
    __tablename__ = "mcp_servers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    access_url = Column(String, nullable=True)
    documentation_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="ACTIVE")
    protocol_version = Column(String, nullable=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    team = relationship("Team", back_populates="mcp_servers")
    tools = relationship("MCPTool", back_populates="server", cascade="all, delete-orphan")
    resources = relationship("MCPResource", back_populates="server", cascade="all, delete-orphan")

class MCPTool(Base):
    __tablename__ = "mcp_tools"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    server_id = Column(UUID(as_uuid=True), ForeignKey("mcp_servers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    input_schema = Column(JSONB, nullable=True)
    category = Column(String, nullable=True)
    
    server = relationship("MCPServer", back_populates="tools")

class MCPResource(Base):
    __tablename__ = "mcp_resources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    server_id = Column(UUID(as_uuid=True), ForeignKey("mcp_servers.id"), nullable=False)
    name = Column(String, nullable=False)
    uri_template = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    mime_type = Column(String, nullable=True)
    
    server = relationship("MCPServer", back_populates="resources")
