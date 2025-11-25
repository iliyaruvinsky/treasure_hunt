from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class IssueType(Base):
    __tablename__ = "issue_types"

    id = Column(Integer, primary_key=True, index=True)
    focus_area_id = Column(Integer, ForeignKey("focus_areas.id"), nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)  # e.g., SOD_VIOLATION, FRAUD_INDICATOR
    name = Column(String, nullable=False)
    description = Column(Text)
    default_severity = Column(String)  # Critical, High, Medium, Low
    
    # Relationships
    focus_area = relationship("FocusArea", backref="issue_types")
    issue_groups = relationship("IssueGroup", back_populates="issue_type")


class IssueGroup(Base):
    __tablename__ = "issue_groups"

    id = Column(Integer, primary_key=True, index=True)
    issue_type_id = Column(Integer, ForeignKey("issue_types.id"), nullable=False)
    analysis_run_id = Column(Integer, ForeignKey("analysis_runs.id"), nullable=False)
    
    # Aggregated data
    finding_count = Column(Integer, default=0)
    total_risk_score = Column(Integer, default=0)
    total_money_loss = Column(Float, default=0.0)
    
    # Summary
    summary = Column(Text)
    
    # Relationships
    issue_type = relationship("IssueType", back_populates="issue_groups")
    analysis_run = relationship("AnalysisRun", backref="issue_groups")

