import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer, Float, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from backend.db.database import Base

class AgentMetric(Base):
    __tablename__ = "agent_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    date = Column(Date, nullable=False)
    invocations = Column(Integer, default=0)
    unique_users = Column(Integer, default=0)
    avg_latency_ms = Column(Float, default=0.0)
    success_rate = Column(Float, default=1.0)
    error_rate = Column(Float, default=0.0)

class DiscoveryLog(Base):
    __tablename__ = "discovery_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    query = Column(Text, nullable=False)
    intent_json = Column(JSONB, nullable=True)
    latency_ms = Column(Integer, default=0)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    feedback = relationship("DiscoveryFeedback", back_populates="discovery_log", uselist=False)

class GuardrailAudit(Base):
    __tablename__ = "guardrail_audits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    original_query = Column(Text, nullable=False)
    violation_type = Column(String, nullable=False) # pii|injection|secret|toxicity
    violation_detail = Column(Text, nullable=True)
    action_taken = Column(String, nullable=False) # blocked|sanitized|flagged
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
