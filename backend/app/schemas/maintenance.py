from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class DeleteRequest(BaseModel):
    """Request model for delete operations"""
    confirm: bool = False


class DeleteResponse(BaseModel):
    """Response model for delete operations"""
    success: bool
    message: str
    deleted_records: Dict[str, int]


class DataSourceSummary(BaseModel):
    """Summary of a data source"""
    id: int
    filename: str
    data_type: str
    status: str
    upload_date: Optional[str]
    findings_count: int
    file_size: Optional[int]


class AuditLogResponse(BaseModel):
    """Audit log entry response"""
    id: int
    action: str
    entity_type: Optional[str]
    entity_id: Optional[int]
    user_id: Optional[str]
    user_ip: Optional[str]
    user_agent: Optional[str]
    description: Optional[str]
    details: Optional[Dict[str, Any]]
    status: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

