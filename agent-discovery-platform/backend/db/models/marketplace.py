import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from backend.db.database import Base

class AgentReview(Base):
    __tablename__ = "agent_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    user_id = Column(String, nullable=False)
    review_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentRating(Base):
    __tablename__ = "agent_ratings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    user_id = Column(String, nullable=False)
    rating = Column(Integer, nullable=False) # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
