from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class SoDAReportMetadata(Base):
    __tablename__ = "soda_report_metadata"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False, unique=True)
    report_type = Column(String, nullable=False, index=True)  # AVR, PVR, ARP, CRV, IVR, etc.
    report_date = Column(DateTime)
    parameters = Column(JSON)  # Parameters sheet data
    kpis = Column(JSON)  # KPIs sheet data
    result_count = Column(Integer)  # Number of results
    
    data_source = relationship("DataSource", backref="soda_report_metadata")


class SoDAReport(Base):
    __tablename__ = "soda_reports"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    
    # Common fields (will vary by report type)
    user_name = Column(String, index=True)
    role_name = Column(String, index=True)
    transaction_code = Column(String)
    authorization_object = Column(String)
    violation_type = Column(String)  # SoD violation, fraud indicator, etc.
    risk_level = Column(String)  # High, Medium, Low
    
    # Raw data stored as JSON
    raw_data = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    data_source = relationship("DataSource", back_populates="reports")
    findings = relationship("Finding", back_populates="soda_report")

