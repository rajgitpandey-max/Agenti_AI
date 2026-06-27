import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.db.database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False, default="DRAFT") # DRAFT|REVIEW|APPROVED|PRODUCTION|DEPRECATED|RETIRED
    classification = Column(String, nullable=False, default="INTERNAL") # PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED
    repo_url = Column(String, nullable=True)
    confluence_url = Column(String, nullable=True)
    tech_stack = Column(ARRAY(String), nullable=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    manifest = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    team = relationship("Team", back_populates="agents")
    versions = relationship("AgentVersion", back_populates="agent", cascade="all, delete-orphan")
    capabilities = relationship("AgentCapability", back_populates="agent", cascade="all, delete-orphan")
    dependencies = relationship("AgentDependency", back_populates="agent", cascade="all, delete-orphan")

class AgentVersion(Base):
    __tablename__ = "agent_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    version = Column(String, nullable=False) # semver
    channel = Column(String, nullable=False, default="stable") # latest|stable|deprecated|experimental
    changelog = Column(Text, nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow)
    
    agent = relationship("Agent", back_populates="versions")

class AgentCapability(Base):
    __tablename__ = "agent_capabilities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    capability = Column(String, nullable=False)
    domain = Column(String, nullable=True)
    
    agent = relationship("Agent", back_populates="capabilities")

class AgentDependency(Base):
    __tablename__ = "agent_dependencies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    dependency_type = Column(String, nullable=False) # agent|tool|model|workflow|knowledge_base|mcp_server
    dependency_ref = Column(String, nullable=False)
    
    agent = relationship("Agent", back_populates="dependencies")
