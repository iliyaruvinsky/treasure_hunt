from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AnalysisRequest(BaseModel):
    data_source_id: int


class AnalysisRunResponse(BaseModel):
    id: int
    run_name: Optional[str]
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_findings: int
    findings_by_focus_area: Optional[Dict[str, int]]
    findings_by_issue_type: Optional[Dict[str, int]]
    total_risk_score: int
    total_money_loss: float
    error_message: Optional[str]
    
    class Config:
        from_attributes = True

