from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"), nullable=False, unique=True)
    
    # Risk scoring
    risk_score = Column(Integer, nullable=False)  # 0-100
    risk_level = Column(String, nullable=False)  # Critical, High, Medium, Low
    
    # Risk details
    risk_category = Column(String)  # Security, Compliance, Operational, Financial
    risk_description = Column(Text)
    risk_factors = Column(JSON)  # List of contributing factors
    
    # Impact assessment
    potential_impact = Column(Text)
    affected_systems = Column(JSON)  # List of affected systems/components
    affected_users = Column(Integer)
    
    # Relationships
    finding = relationship("Finding", back_populates="risk_assessment")

