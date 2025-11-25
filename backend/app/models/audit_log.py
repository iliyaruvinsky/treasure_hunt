from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from app.core.database import Base
from datetime import datetime


class AuditLog(Base):
    """Audit log for tracking user actions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Action details
    action = Column(String, nullable=False)  # upload, delete, analyze, etc.
    entity_type = Column(String)  # data_source, finding, analysis_run, etc.
    entity_id = Column(Integer)  # ID of the affected entity
    
    # User information
    user_id = Column(String)  # Can be extended to support actual user auth
    user_ip = Column(String)
    user_agent = Column(String)
    
    # Action details
    description = Column(Text)  # Human-readable description
    details = Column(JSON)  # Additional structured data
    
    # Result
    status = Column(String)  # success, error, partial
    error_message = Column(Text)  # If status is error
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

