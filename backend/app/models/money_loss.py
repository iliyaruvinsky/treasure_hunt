from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class MoneyLossCalculation(Base):
    __tablename__ = "money_loss_calculations"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"), nullable=False, unique=True)
    
    # Calculation results
    estimated_loss = Column(Float, nullable=False)  # In currency units
    confidence_score = Column(Float)  # 0.0 to 1.0
    calculation_method = Column(String)  # llm, ml, hybrid
    
    # Breakdown
    llm_estimate = Column(Float)  # LLM-based estimate
    ml_estimate = Column(Float)  # ML-based estimate
    final_estimate = Column(Float)  # Combined/hybrid estimate
    
    # Calculation details
    calculation_details = Column(JSON)  # Detailed breakdown
    reasoning = Column(Text)  # LLM reasoning for the calculation
    factors_considered = Column(JSON)  # List of factors
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    finding = relationship("Finding", back_populates="money_loss_calculation")

