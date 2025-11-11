from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class DataSourceType(str, enum.Enum):
    ALERT = "alert"
    REPORT = "report"


class FileFormat(str, enum.Enum):
    PDF = "pdf"
    CSV = "csv"
    DOCX = "docx"
    XLSX = "xlsx"
    JSON = "json"


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False, index=True)
    original_filename = Column(String, nullable=False)
    file_format = Column(SQLEnum(FileFormat), nullable=False)
    data_type = Column(SQLEnum(DataSourceType), nullable=False)
    file_size = Column(Integer)  # in bytes
    file_path = Column(String, nullable=False)  # Path to stored file
    alert_id = Column(String, index=True)  # For 4C alerts: SLG_XXXXXX_XXXXXX
    report_type = Column(String)  # For SoDA reports: AVR, PVR, etc.
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    uploaded_by = Column(String)  # User who uploaded (if auth implemented)
    status = Column(String, default="pending")  # pending, processing, completed, error
    error_message = Column(String)
    
    # Relationships
    alerts = relationship("Alert", back_populates="data_source")
    reports = relationship("SoDAReport", back_populates="data_source")
    findings = relationship("Finding", back_populates="data_source")

