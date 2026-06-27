import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.db.database import Base

class Certification(Base):
    __tablename__ = "certifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    review_type = Column(String, nullable=False) # security|responsible_ai|architecture|compliance
    status = Column(String, nullable=False, default="pending") # pending|approved|rejected
    reviewer = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
