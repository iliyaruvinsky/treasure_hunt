from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.models.data_source import DataSource
from app.models.finding import Finding
from app.models.analysis_run import AnalysisRun
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata
from app.models.risk_assessment import RiskAssessment
from app.models.money_loss import MoneyLossCalculation
from app.models.audit_log import AuditLog
from app.models.issue_type import IssueGroup
from app.schemas.maintenance import (
    DeleteRequest,
    DeleteResponse,
    AuditLogResponse,
    DataSourceSummary
)
from app.utils.audit_logger import audit_log

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("/data-sources", response_model=List[DataSourceSummary])
async def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all data sources with summary information"""
    data_sources = db.query(DataSource).order_by(
        DataSource.upload_date.desc()
    ).offset(skip).limit(limit).all()
    
    result = []
    for ds in data_sources:
        findings_count = db.query(Finding).filter(
            Finding.data_source_id == ds.id
        ).count()
        
        result.append(DataSourceSummary(
            id=ds.id,
            filename=ds.filename,
            data_type=ds.data_type,
            status=ds.status,
            upload_date=ds.upload_date.isoformat() if ds.upload_date else None,
            findings_count=findings_count,
            file_size=ds.file_size
        ))
    
    return result


@router.delete("/data-sources/{data_source_id}", response_model=DeleteResponse)
async def delete_data_source(
    data_source_id: int,
    db: Session = Depends(get_db),
    request: Optional[DeleteRequest] = None
):
    """Delete a data source and all related data"""
    data_source = db.query(DataSource).filter(
        DataSource.id == data_source_id
    ).first()
    
    if not data_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data source {data_source_id} not found"
        )
    
    try:
        # Count related records for audit log
        findings_count = db.query(Finding).filter(
            Finding.data_source_id == data_source_id
        ).count()
        alerts_count = db.query(Alert).filter(
            Alert.data_source_id == data_source_id
        ).count()
        reports_count = db.query(SoDAReport).filter(
            SoDAReport.data_source_id == data_source_id
        ).count()
        analysis_run_ids = [
            run_id for (run_id,) in db.query(AnalysisRun.id).filter(
                AnalysisRun.data_source_id == data_source_id
            ).all()
        ]
        issue_group_count = 0
        if analysis_run_ids:
            issue_group_count = db.query(IssueGroup).filter(
                IssueGroup.analysis_run_id.in_(analysis_run_ids)
            ).count()
        
        # Delete related data in correct order (respecting foreign keys)
        # 1. Delete money loss calculations
        db.query(MoneyLossCalculation).filter(
            MoneyLossCalculation.finding_id.in_(
                db.query(Finding.id).filter(Finding.data_source_id == data_source_id)
            )
        ).delete(synchronize_session=False)
        
        # 2. Delete risk assessments
        db.query(RiskAssessment).filter(
            RiskAssessment.finding_id.in_(
                db.query(Finding.id).filter(Finding.data_source_id == data_source_id)
            )
        ).delete(synchronize_session=False)
        
        # 3. Delete findings
        db.query(Finding).filter(
            Finding.data_source_id == data_source_id
        ).delete(synchronize_session=False)
        
        # 4. Delete issue groups tied to analysis runs, then the runs themselves
        if analysis_run_ids:
            db.query(IssueGroup).filter(
                IssueGroup.analysis_run_id.in_(analysis_run_ids)
            ).delete(synchronize_session=False)
            db.query(AnalysisRun).filter(
                AnalysisRun.id.in_(analysis_run_ids)
            ).delete(synchronize_session=False)
        
        # 5. Delete alert metadata and alerts
        alert_metadata = db.query(AlertMetadata).filter(
            AlertMetadata.data_source_id == data_source_id
        ).first()
        if alert_metadata:
            db.query(Alert).filter(
                Alert.data_source_id == data_source_id
            ).delete(synchronize_session=False)
            db.delete(alert_metadata)
        
        # 6. Delete report metadata and reports
        report_metadata = db.query(SoDAReportMetadata).filter(
            SoDAReportMetadata.data_source_id == data_source_id
        ).first()
        if report_metadata:
            db.query(SoDAReport).filter(
                SoDAReport.data_source_id == data_source_id
            ).delete(synchronize_session=False)
            db.delete(report_metadata)
        
        # 7. Delete the data source itself
        filename = data_source.filename
        db.delete(data_source)
        db.commit()
        
        # Log the deletion
        audit_log(
            db=db,
            action="delete",
            entity_type="data_source",
            entity_id=data_source_id,
            description=f"Deleted data source: {filename}",
            details={
                "filename": filename,
                "findings_deleted": findings_count,
                "alerts_deleted": alerts_count,
                "reports_deleted": reports_count,
                "analysis_runs_deleted": len(analysis_run_ids),
                "issue_groups_deleted": issue_group_count
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message=f"Data source {data_source_id} and all related data deleted successfully",
            deleted_records={
                "data_source": 1,
                "findings": findings_count,
                "alerts": alerts_count,
                "reports": reports_count
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting data source {data_source_id}: {str(e)}")
        
        # Log the error
        audit_log(
            db=db,
            action="delete",
            entity_type="data_source",
            entity_id=data_source_id,
            description=f"Failed to delete data source: {data_source.filename}",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting data source: {str(e)}"
        )


@router.delete("/data-sources", response_model=DeleteResponse)
async def delete_all_data_sources(
    confirm: bool = Query(False, description="Must be True to confirm deletion"),
    db: Session = Depends(get_db)
):
    """Delete ALL data sources and all related data"""
    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must set confirm=true to delete all data"
        )
    
    try:
        # Count all records
        total_data_sources = db.query(DataSource).count()
        total_findings = db.query(Finding).count()
        total_alerts = db.query(Alert).count()
        total_reports = db.query(SoDAReport).count()
        total_issue_groups = db.query(IssueGroup).count()
        total_analysis_runs = db.query(AnalysisRun).count()
        
        # Delete all data (same order as single deletion)
        db.query(MoneyLossCalculation).delete()
        db.query(RiskAssessment).delete()
        db.query(Finding).delete()
        db.query(IssueGroup).delete()
        db.query(AnalysisRun).delete()
        db.query(Alert).delete()
        db.query(SoDAReport).delete()
        db.query(AlertMetadata).delete()
        db.query(SoDAReportMetadata).delete()
        db.query(DataSource).delete()
        
        db.commit()
        
        # Log the deletion
        audit_log(
            db=db,
            action="delete_all",
            entity_type="data_source",
            description="Deleted all data sources and related data",
            details={
                "data_sources_deleted": total_data_sources,
                "findings_deleted": total_findings,
                "alerts_deleted": total_alerts,
                "reports_deleted": total_reports,
                "analysis_runs_deleted": total_analysis_runs,
                "issue_groups_deleted": total_issue_groups
            },
            status="success"
        )
        
        return DeleteResponse(
            success=True,
            message="All data sources and related data deleted successfully",
            deleted_records={
                "data_source": total_data_sources,
                "findings": total_findings,
                "alerts": total_alerts,
                "reports": total_reports,
                "analysis_runs": total_analysis_runs,
                "issue_groups": total_issue_groups
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting all data sources: {str(e)}")
        
        audit_log(
            db=db,
            action="delete_all",
            entity_type="data_source",
            description="Failed to delete all data sources",
            status="error",
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting all data sources: {str(e)}"
        )


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get audit logs with optional filters"""
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if status_filter:
        query = query.filter(AuditLog.status == status_filter)
    
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return [AuditLogResponse.model_validate(log) for log in logs]


@router.get("/logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific audit log entry"""
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found"
        )
    return AuditLogResponse.model_validate(log)

