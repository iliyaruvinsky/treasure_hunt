from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import traceback
import logging

from app.core.database import get_db
from app.services.analysis.analyzer import Analyzer
from app.models.analysis_run import AnalysisRun
from app.models.finding import Finding
from app.models.focus_area import FocusArea
from app.schemas.analysis import AnalysisRunResponse, AnalysisRequest
from app.utils.audit_logger import audit_log

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.options("/run")
async def options_analysis_run():
    """Handle OPTIONS preflight request"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3001",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )


@router.post("/run", response_model=AnalysisRunResponse)
async def run_analysis(
    request: AnalysisRequest,
    http_request: Request = None,
    db: Session = Depends(get_db)
):
    """Run analysis on a data source"""
    analyzer = Analyzer(db)
    
    try:
        analysis_run = analyzer.analyze_data_source(request.data_source_id)
        
        # Log the analysis
        try:
            user_ip = http_request.client.host if http_request and hasattr(http_request, 'client') else None
            user_agent = http_request.headers.get("user-agent") if http_request else None
        except:
            user_ip = None
            user_agent = None
        audit_log(
            db=db,
            action="analyze",
            entity_type="data_source",
            entity_id=request.data_source_id,
            user_ip=user_ip,
            user_agent=user_agent,
            description=f"Analysis run completed for data source {request.data_source_id}",
            details={
                "analysis_run_id": analysis_run.id,
                "total_findings": analysis_run.total_findings,
                "total_risk_score": analysis_run.total_risk_score,
                "total_money_loss": analysis_run.total_money_loss,
                "status": analysis_run.status
            },
            status="success" if analysis_run.status == "completed" else "error",
            error_message=analysis_run.error_message if analysis_run.status == "error" else None
        )
        
        return AnalysisRunResponse.model_validate(analysis_run)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        # Log full traceback for debugging
        error_traceback = traceback.format_exc()
        logger.error(f"Analysis failed: {str(e)}\n{error_traceback}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/runs", response_model=List[AnalysisRunResponse])
async def list_analysis_runs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all analysis runs"""
    runs = db.query(AnalysisRun).order_by(
        AnalysisRun.started_at.desc()
    ).offset(skip).limit(limit).all()
    return [AnalysisRunResponse.model_validate(run) for run in runs]


@router.get("/runs/{run_id}", response_model=AnalysisRunResponse)
async def get_analysis_run(
    run_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific analysis run"""
    run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis run not found"
        )
    return AnalysisRunResponse.model_validate(run)


@router.get("/findings")
async def get_findings(
    focus_area: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10000,  # Increased limit to handle large datasets
    db: Session = Depends(get_db)
):
    """Get findings with optional filters"""
    from sqlalchemy.orm import joinedload
    
    query = db.query(Finding).options(
        joinedload(Finding.focus_area),
        joinedload(Finding.issue_type),
        joinedload(Finding.risk_assessment),
        joinedload(Finding.money_loss_calculation)
    )
    
    if focus_area:
        focus_area_obj = db.query(FocusArea).filter(FocusArea.code == focus_area).first()
        if focus_area_obj:
            query = query.filter(Finding.focus_area_id == focus_area_obj.id)
    
    if severity:
        query = query.filter(Finding.severity == severity)
    
    if status:
        query = query.filter(Finding.status == status)
    
    if date_from:
        from datetime import datetime
        query = query.filter(Finding.detected_at >= datetime.fromisoformat(date_from))
    
    if date_to:
        from datetime import datetime
        query = query.filter(Finding.detected_at <= datetime.fromisoformat(date_to))
    
    findings = query.order_by(Finding.detected_at.desc()).offset(skip).limit(limit).all()
    
    # Convert to response format with relationships
    result = []
    for finding in findings:
        finding_dict = {
            "id": finding.id,
            "title": finding.title,
            "description": finding.description,
            "severity": finding.severity,
            "status": finding.status,
            "detected_at": finding.detected_at.isoformat() if finding.detected_at else None,
            "focus_area": {
                "code": finding.focus_area.code if finding.focus_area else None,
                "name": finding.focus_area.name if finding.focus_area else None,
            },
            "issue_type": {
                "code": finding.issue_type.code if finding.issue_type else None,
                "name": finding.issue_type.name if finding.issue_type else None,
            } if finding.issue_type else None,
        }
        
        if finding.risk_assessment:
            finding_dict["risk_assessment"] = {
                "risk_score": int(finding.risk_assessment.risk_score) if finding.risk_assessment.risk_score else 0,
                "risk_level": finding.risk_assessment.risk_level,
            }
        else:
            finding_dict["risk_assessment"] = None
        
        if finding.money_loss_calculation:
            finding_dict["money_loss_calculation"] = {
                "estimated_loss": float(finding.money_loss_calculation.estimated_loss) if finding.money_loss_calculation.estimated_loss else 0.0,
                "confidence": float(finding.money_loss_calculation.confidence_score) if finding.money_loss_calculation.confidence_score else 0.0,
            }
        else:
            finding_dict["money_loss_calculation"] = None
        
        result.append(finding_dict)
    
    return result

