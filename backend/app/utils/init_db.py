"""
Database initialization script
Creates tables and seeds initial data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import Base, engine, SessionLocal
from app.models.focus_area import FocusArea
from app.models.issue_type import IssueType


def init_focus_areas(db: Session):
    """Initialize the 6 focus areas"""
    focus_areas = [
        {
            "code": "BUSINESS_PROTECTION",
            "name": "Business Protection",
            "description": "Fraud detection, cybersecurity protection and prevention"
        },
        {
            "code": "BUSINESS_CONTROL",
            "name": "Business Control",
            "description": "Business bottlenecks detection, process observability, business anomalies detection"
        },
        {
            "code": "ACCESS_GOVERNANCE",
            "name": "Access Governance",
            "description": "Segregation of Duties governance, authorizations control, user access and risk reviews"
        },
        {
            "code": "TECHNICAL_CONTROL",
            "name": "Technical Control",
            "description": "Infrastructure observability, communications and interfaces, technical anomalies detection"
        },
        {
            "code": "JOBS_CONTROL",
            "name": "Jobs Control",
            "description": "Jobs performance deep analysis, resource utilization analysis, anomalies tracking"
        },
        {
            "code": "S4HANA_EXCELLENCE",
            "name": "S/4HANA Excellence",
            "description": "Post go-live protection, post migration safeguarding, business continuity"
        }
    ]
    
    for fa_data in focus_areas:
        existing = db.query(FocusArea).filter(FocusArea.code == fa_data["code"]).first()
        if not existing:
            focus_area = FocusArea(**fa_data)
            db.add(focus_area)
    
    db.commit()


def init_issue_types(db: Session):
    """Initialize common issue types for each focus area"""
    issue_types = [
        # Business Protection
        {
            "focus_area_code": "BUSINESS_PROTECTION",
            "code": "FRAUD_DETECTION",
            "name": "Fraud Detection",
            "description": "Detected potential fraud indicators",
            "default_severity": "Critical"
        },
        {
            "focus_area_code": "BUSINESS_PROTECTION",
            "code": "CYBERSECURITY_THREAT",
            "name": "Cybersecurity Threat",
            "description": "Potential cybersecurity threats detected",
            "default_severity": "Critical"
        },
        {
            "focus_area_code": "BUSINESS_PROTECTION",
            "code": "MATERIAL_CONVERSION_FRAUD",
            "name": "Material Conversion Fraud",
            "description": "High-value materials converted to low-value items",
            "default_severity": "Critical"
        },
        {
            "focus_area_code": "BUSINESS_PROTECTION",
            "code": "VENDOR_PAYMENT_DIVERSION",
            "name": "Vendor Payment Diversion",
            "description": "Bank account changes followed by quick reversals",
            "default_severity": "Critical"
        },
        # Business Control
        {
            "focus_area_code": "BUSINESS_CONTROL",
            "code": "PROCESS_BOTTLENECK",
            "name": "Process Bottleneck",
            "description": "Business process bottlenecks causing delays",
            "default_severity": "High"
        },
        {
            "focus_area_code": "BUSINESS_CONTROL",
            "code": "UNBILLED_DELIVERY",
            "name": "Unbilled Delivery",
            "description": "Goods shipped but not invoiced",
            "default_severity": "High"
        },
        {
            "focus_area_code": "BUSINESS_CONTROL",
            "code": "DATA_EXCHANGE_FAILURE",
            "name": "Data Exchange Failure",
            "description": "Critical business data transmission breakdowns",
            "default_severity": "High"
        },
        # Access Governance
        {
            "focus_area_code": "ACCESS_GOVERNANCE",
            "code": "SOD_VIOLATION",
            "name": "Segregation of Duties Violation",
            "description": "User has conflicting permissions enabling fraud",
            "default_severity": "Critical"
        },
        {
            "focus_area_code": "ACCESS_GOVERNANCE",
            "code": "UNAUTHORIZED_ACCESS",
            "name": "Unauthorized Access",
            "description": "User accessing systems without proper authorization",
            "default_severity": "Critical"
        },
        {
            "focus_area_code": "ACCESS_GOVERNANCE",
            "code": "LONG_SESSION",
            "name": "Long Session Duration",
            "description": "User logged in for extended period (24+ hours)",
            "default_severity": "Medium"
        },
        {
            "focus_area_code": "ACCESS_GOVERNANCE",
            "code": "SELF_APPROVAL",
            "name": "Self-Approval Violation",
            "description": "User approving their own transactions",
            "default_severity": "High"
        },
        # Technical Control
        {
            "focus_area_code": "TECHNICAL_CONTROL",
            "code": "SYSTEM_DUMP",
            "name": "System Dump",
            "description": "ABAP runtime errors indicating system issues",
            "default_severity": "High"
        },
        {
            "focus_area_code": "TECHNICAL_CONTROL",
            "code": "LOCK_CONFLICT",
            "name": "Application Lock Conflict",
            "description": "Prolonged locks causing performance bottlenecks",
            "default_severity": "Medium"
        },
        {
            "focus_area_code": "TECHNICAL_CONTROL",
            "code": "RESOURCE_EXHAUSTION",
            "name": "Resource Exhaustion",
            "description": "Low CPU, memory, or disk space",
            "default_severity": "High"
        },
        # Jobs Control
        {
            "focus_area_code": "JOBS_CONTROL",
            "code": "LONG_RUNNING_JOB",
            "name": "Long-Running Background Job",
            "description": "Job running abnormally long (24+ hours)",
            "default_severity": "Medium"
        },
        {
            "focus_area_code": "JOBS_CONTROL",
            "code": "JOB_FAILURE",
            "name": "Job Processing Failure",
            "description": "Failed batch processes affecting operations",
            "default_severity": "High"
        },
        # S/4HANA Excellence
        {
            "focus_area_code": "S4HANA_EXCELLENCE",
            "code": "MIGRATION_ISSUE",
            "name": "Post-Migration Issue",
            "description": "Issues detected after S/4HANA migration",
            "default_severity": "High"
        },
        {
            "focus_area_code": "S4HANA_EXCELLENCE",
            "code": "FIORI_ADOPTION",
            "name": "Fiori Interface Adoption",
            "description": "User adaptation tracking for new interface",
            "default_severity": "Low"
        }
    ]
    
    for it_data in issue_types:
        focus_area = db.query(FocusArea).filter(
            FocusArea.code == it_data.pop("focus_area_code")
        ).first()
        
        if focus_area:
            existing = db.query(IssueType).filter(
                IssueType.code == it_data["code"]
            ).first()
            
            if not existing:
                issue_type = IssueType(
                    focus_area_id=focus_area.id,
                    **it_data
                )
                db.add(issue_type)
    
    db.commit()


def init_database():
    """Initialize database with tables and seed data"""
    # Import all models to ensure they're registered with Base
    from app.models.audit_log import AuditLog
    from app.models.data_source import DataSource
    from app.models.finding import Finding
    from app.models.analysis_run import AnalysisRun
    from app.models.risk_assessment import RiskAssessment
    from app.models.money_loss import MoneyLossCalculation
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Ensure new columns/indexes exist for backward compatibility
    with engine.connect() as connection:
        connection.execute(
            text(
                "ALTER TABLE IF EXISTS analysis_runs "
                "ADD COLUMN IF NOT EXISTS data_source_id INTEGER"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_analysis_runs_data_source_id "
                "ON analysis_runs (data_source_id)"
            )
        )
    
    # Seed initial data
    db = SessionLocal()
    try:
        init_focus_areas(db)
        init_issue_types(db)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

