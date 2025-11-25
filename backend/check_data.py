#!/usr/bin/env python3
"""Quick script to check database statistics"""
from app.core.database import SessionLocal
from app.models.finding import Finding
from app.models.risk_assessment import RiskAssessment
from app.models.money_loss import MoneyLossCalculation
from sqlalchemy import func

db = SessionLocal()

try:
    # Count findings
    total_findings = db.query(Finding).count()
    print(f"Total Findings: {total_findings}")
    
    # Check sample finding
    sample = db.query(Finding).first()
    if sample:
        print(f"\nSample Finding:")
        print(f"  ID: {sample.id}")
        print(f"  Title: {sample.title}")
        print(f"  Has risk_assessment: {sample.risk_assessment is not None}")
        if sample.risk_assessment:
            print(f"  Risk Score: {sample.risk_assessment.risk_score}")
        print(f"  Has money_loss_calculation: {sample.money_loss_calculation is not None}")
        if sample.money_loss_calculation:
            print(f"  Estimated Loss: {sample.money_loss_calculation.estimated_loss}")
    
    # Calculate total risk score
    total_risk = db.query(func.sum(RiskAssessment.risk_score)).scalar() or 0
    print(f"\nTotal Risk Score (sum): {total_risk}")
    
    # Count findings with risk assessments
    findings_with_risk = db.query(Finding).join(RiskAssessment).count()
    print(f"Findings with Risk Assessment: {findings_with_risk}")
    
    # Calculate total money loss
    total_money = db.query(func.sum(MoneyLossCalculation.estimated_loss)).scalar() or 0
    print(f"Total Money Loss (sum): {total_money}")
    
    # Count findings with money loss
    findings_with_money = db.query(Finding).join(MoneyLossCalculation).count()
    print(f"Findings with Money Loss: {findings_with_money}")
    
finally:
    db.close()

