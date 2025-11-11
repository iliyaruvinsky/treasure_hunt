from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.data_source import DataSourceType, FileFormat


class DataSourceResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_format: str
    data_type: str
    file_size: Optional[int]
    alert_id: Optional[str]
    report_type: Optional[str]
    upload_date: datetime
    status: str
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    data_source_id: int
    filename: str
    status: str
    parse_result: Dict[str, Any]
    
    class Config:
        from_attributes = True

