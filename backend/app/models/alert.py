from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class AlertMetadata(Base):
    __tablename__ = "alert_metadata"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False, unique=True)
    alert_name = Column(String, nullable=False, index=True)
    alert_id = Column(String, index=True)  # SLG_XXXXXX_XXXXXX
    parameters = Column(JSON)  # Alert Parameters sheet data
    filter_criteria = Column(JSON)  # Extracted filter conditions
    
    data_source = relationship("DataSource", backref="alert_metadata")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    
    # Normalized fields from Skywind 4C alerts
    application_server = Column(String)
    user_name = Column(String, index=True)
    full_name = Column(String)
    client = Column(String)
    terminal = Column(String)
    transaction_code = Column(String)
    timestamp = Column(DateTime, index=True)
    duration = Column(Integer)  # Duration in time units
    duration_unit = Column(String)  # M, H, D
    ip_address = Column(String)
    memory_consumption = Column(Integer)  # MB
    date = Column(DateTime)
    
    # Raw data stored as JSON for reference
    raw_data = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    data_source = relationship("DataSource", back_populates="alerts")
    findings = relationship("Finding", back_populates="alert")

