from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.data_source import DataSource, DataSourceType, FileFormat
from app.services.ingestion.parser_factory import ParserFactory
from app.services.ingestion.data_saver import DataSaver
from app.schemas.ingestion import DataSourceResponse, UploadResponse
from pydantic import BaseModel

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse a file (PDF, CSV, DOCX, Excel)"""
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    # Check if parser can handle this file
    if not ParserFactory.can_parse_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file.filename}"
        )
    
    # Determine file format
    file_ext = Path(file.filename).suffix.lower().lstrip('.')
    try:
        file_format = FileFormat(file_ext)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {file_ext}"
        )
    
    # Determine data type (alert or report)
    # This is a simple heuristic - can be improved
    filename_lower = file.filename.lower()
    if 'alert' in filename_lower or 'slg_' in filename_lower:
        data_type = DataSourceType.ALERT
    else:
        data_type = DataSourceType.REPORT
    
    # Create storage directory if it doesn't exist
    storage_path = Path(settings.STORAGE_PATH)
    storage_path.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = storage_path / f"{datetime.utcnow().timestamp()}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Create data source record
    data_source = DataSource(
        filename=file.filename,
        original_filename=file.filename,
        file_format=file_format,
        data_type=data_type,
        file_size=file_size,
        file_path=str(file_path),
        status="pending"
    )
    
    db.add(data_source)
    db.commit()
    db.refresh(data_source)
    
    # Parse file
    parser = ParserFactory.get_parser(str(file_path))
    if not parser:
        data_source.status = "error"
        data_source.error_message = "No parser available for this file"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No parser available for this file"
        )
    
    try:
        parse_result = parser.parse(str(file_path))
        
        # Update data source with metadata
        if parse_result.get('metadata'):
            metadata = parse_result['metadata']
            
            # Extract alert_id or report_type from metadata
            if 'alert_id' in metadata:
                data_source.alert_id = metadata['alert_id']
            if 'report_type' in metadata:
                data_source.report_type = metadata['report_type']
        
        # Save parsed data to database
        data_saver = DataSaver(db)
        if data_source.data_type == DataSourceType.ALERT:
            try:
                data_saver.save_4c_alert(data_source, parse_result)
            except Exception as e:
                parse_result['errors'] = parse_result.get('errors', []) + [f"Error saving alerts: {str(e)}"]
        elif data_source.data_type == DataSourceType.REPORT:
            try:
                data_saver.save_soda_report(data_source, parse_result)
            except Exception as e:
                parse_result['errors'] = parse_result.get('errors', []) + [f"Error saving reports: {str(e)}"]
        
        data_source.status = "completed" if not parse_result.get('errors') else "error"
        if parse_result.get('errors'):
            data_source.error_message = '; '.join(parse_result['errors'])
        
        db.commit()
        
        return UploadResponse(
            data_source_id=data_source.id,
            filename=file.filename or "unknown",
            status=data_source.status,
            parse_result=parse_result
        )
        
    except Exception as e:
        data_source.status = "error"
        data_source.error_message = str(e)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing file: {str(e)}"
        )


@router.get("/data-sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all uploaded data sources"""
    data_sources = db.query(DataSource).offset(skip).limit(limit).all()
    return [DataSourceResponse.model_validate(ds) for ds in data_sources]


@router.get("/data-sources/{data_source_id}", response_model=DataSourceResponse)
async def get_data_source(
    data_source_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific data source"""
    data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
    if not data_source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    return DataSourceResponse.model_validate(data_source)

