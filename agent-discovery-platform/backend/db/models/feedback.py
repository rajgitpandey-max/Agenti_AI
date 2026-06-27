import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.db.database import Base

class DiscoveryFeedback(Base):
    __tablename__ = "discovery_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    discovery_log_id = Column(UUID(as_uuid=True), ForeignKey("discovery_logs.id"), nullable=False)
    user_id = Column(String, nullable=False)
    feedback_type = Column(String, nullable=False) # thumbs_up|thumbs_down|correction
    selected_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    correction_text = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True) # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    
    discovery_log = relationship("DiscoveryLog", back_populates="feedback")
    
class FeedbackAggregate(Base):
    __tablename__ = "feedback_aggregates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_pattern = Column(String, nullable=False)
    total_searches = Column(Integer, default=0)
    thumbs_up_count = Column(Integer, default=0)
    thumbs_down_count = Column(Integer, default=0)
    avg_satisfaction = Column(Float, default=0.0)
    top_selected_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
