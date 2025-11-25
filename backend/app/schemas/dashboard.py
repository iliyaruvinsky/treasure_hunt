from pydantic import BaseModel


class KPISummaryResponse(BaseModel):
    total_findings: int
    total_risk_score: float
    total_money_loss: float
    analysis_runs: int
