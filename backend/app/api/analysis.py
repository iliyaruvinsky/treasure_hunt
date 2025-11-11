from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.analysis.analyzer import Analyzer
from app.models.analysis_run import AnalysisRun
from app.schemas.analysis import AnalysisRunResponse, AnalysisRequest

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run", response_model=AnalysisRunResponse)
async def run_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Run analysis on a data source"""
    analyzer = Analyzer(db)
    
    try:
        analysis_run = analyzer.analyze_data_source(request.data_source_id)
        return AnalysisRunResponse.model_validate(analysis_run)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
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

