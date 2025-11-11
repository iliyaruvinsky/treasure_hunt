from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    soda_report_id = Column(Integer, ForeignKey("soda_reports.id"), nullable=True)
    focus_area_id = Column(Integer, ForeignKey("focus_areas.id"), nullable=False)
    issue_type_id = Column(Integer, ForeignKey("issue_types.id"), nullable=True)
    
    # Finding details
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String)  # Critical, High, Medium, Low
    status = Column(String, default="new")  # new, in_progress, resolved, false_positive
    
    # Classification
    classification_confidence = Column(Float)  # 0.0 to 1.0
    
    # Timestamps
    detected_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    data_source = relationship("DataSource", back_populates="findings")
    alert = relationship("Alert", back_populates="findings")
    soda_report = relationship("SoDAReport", back_populates="findings")
    focus_area = relationship("FocusArea", backref="findings")
    issue_type = relationship("IssueType", backref="findings")
    risk_assessment = relationship("RiskAssessment", back_populates="finding", uselist=False)
    money_loss_calculation = relationship("MoneyLossCalculation", back_populates="finding", uselist=False)

