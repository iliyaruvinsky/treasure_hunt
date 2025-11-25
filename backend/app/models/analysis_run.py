from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), index=True, nullable=True)
    
    # Run metadata
    run_name = Column(String)
    status = Column(String, default="running")  # running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Results summary
    total_findings = Column(Integer, default=0)
    findings_by_focus_area = Column(JSON)  # Count per focus area
    findings_by_issue_type = Column(JSON)  # Count per issue type
    total_risk_score = Column(Integer, default=0)
    total_money_loss = Column(Float, default=0.0)
    
    # Configuration
    analysis_config = Column(JSON)  # Configuration used for this run
    error_message = Column(Text)

    # Relationships
    data_source = relationship("DataSource", back_populates="analysis_runs")

