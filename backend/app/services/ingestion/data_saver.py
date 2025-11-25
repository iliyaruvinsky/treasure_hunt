"""
Service to save parsed data to database
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime
import re
import json
import math

from app.models.data_source import DataSource
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata


class DataSaver:
    """Save parsed data to database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _clean_json_value(self, value: Any) -> Any:
        """Clean value for JSON serialization (replace NaN, Infinity with null)"""
        # Handle float special values
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return None
            # Check for very large numbers that might cause JSON issues
            if abs(value) > 1e308:
                return None
        # Handle numpy/pandas types
        elif hasattr(value, 'item'):  # numpy scalar
            try:
                return self._clean_json_value(value.item())
            except (ValueError, OverflowError):
                return None
        elif isinstance(value, dict):
            return {k: self._clean_json_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._clean_json_value(item) for item in value]
        # Handle other non-serializable types
        try:
            json.dumps(value)  # Test if serializable
            return value
        except (TypeError, ValueError, OverflowError):
            return str(value) if value is not None else None
    
    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a record by replacing NaN/Infinity values with null"""
        return {k: self._clean_json_value(v) for k, v in record.items()}
    
    def save_4c_alert(self, data_source: DataSource, parse_result: Dict[str, Any]):
        """Save 4C alert data to database"""
        metadata = parse_result.get('metadata', {})
        data = parse_result.get('data', [])
        
        # Save alert metadata
        alert_metadata = AlertMetadata(
            data_source_id=data_source.id,
            alert_name=metadata.get('alert_name', ''),
            alert_id=metadata.get('alert_id'),
            parameters=metadata.get('parameters', {}),
            filter_criteria=metadata.get('parameters', {}).get('filters', [])
        )
        self.db.add(alert_metadata)
        self.db.flush()
        
        # Save alert records
        # Note: All fields from source file (up to 100+) are preserved in raw_data JSON column
        from app.core.config import settings
        
        # Apply limit if configured
        records_to_process = data
        if settings.MAX_RECORDS_PER_FILE:
            records_to_process = data[:settings.MAX_RECORDS_PER_FILE]
        
        # Process in batches to avoid memory issues
        batch_size = settings.BATCH_SIZE
        total_records = len(records_to_process)
        
        for i in range(0, total_records, batch_size):
            batch = records_to_process[i:i + batch_size]
            for record in batch:
                # Clean record to remove NaN values (preserves all fields)
                cleaned_record = self._clean_record(record)  # All fields preserved
                alert = self._parse_alert_record(cleaned_record)  # Only extracts common fields
                alert.data_source_id = data_source.id
                alert.raw_data = cleaned_record  # Complete record with all fields stored here
                self.db.add(alert)
            
            # Commit batch to avoid large transactions
            self.db.commit()
        
        # Update metadata with actual count saved
        if settings.MAX_RECORDS_PER_FILE and len(data) > settings.MAX_RECORDS_PER_FILE:
            alert_metadata.result_count = len(records_to_process)
            self.db.commit()
    
    def save_soda_report(self, data_source: DataSource, parse_result: Dict[str, Any]):
        """Save SoDA report data to database"""
        metadata = parse_result.get('metadata', {})
        data = parse_result.get('data', [])
        
        # Save report metadata
        report_date = None
        if metadata.get('report_date'):
            try:
                report_date = datetime.fromisoformat(metadata['report_date'])
            except:
                pass
        
        report_metadata = SoDAReportMetadata(
            data_source_id=data_source.id,
            report_type=metadata.get('report_type', 'UNKNOWN'),
            report_date=report_date,
            parameters=metadata.get('parameters', {}),
            kpis=metadata.get('kpis', {}),
            result_count=len(data)
        )
        self.db.add(report_metadata)
        self.db.flush()
        
        # Save report records
        # Note: All fields from source file (up to 100+) are preserved in raw_data JSON column
        from app.core.config import settings
        
        # Apply limit if configured
        records_to_process = data
        if settings.MAX_RECORDS_PER_FILE:
            records_to_process = data[:settings.MAX_RECORDS_PER_FILE]
        
        # Process in batches to avoid memory issues
        batch_size = settings.BATCH_SIZE
        total_records = len(records_to_process)
        
        for i in range(0, total_records, batch_size):
            batch = records_to_process[i:i + batch_size]
            for record in batch:
                # Clean record to remove NaN values (preserves all fields)
                cleaned_record = self._clean_record(record)  # All fields preserved
                report = self._parse_soda_record(cleaned_record, metadata.get('report_type'))  # Only extracts common fields
                report.data_source_id = data_source.id
                report.raw_data = cleaned_record  # Complete record with all fields stored here
                self.db.add(report)
            
            # Commit batch to avoid large transactions
            self.db.commit()
        
        # Update metadata with actual count saved
        if settings.MAX_RECORDS_PER_FILE and len(data) > settings.MAX_RECORDS_PER_FILE:
            report_metadata.result_count = len(records_to_process)
            self.db.commit()
    
    def _parse_alert_record(self, record: Dict[str, Any]) -> Alert:
        """Parse a single alert record"""
        # Map fields from Skywind 4C format
        alert = Alert()
        
        # Try to extract timestamp from first column
        timestamp_str = record.get('Data', '') or record.get(list(record.keys())[0] if record else '', '')
        if timestamp_str:
            alert.timestamp = self._parse_timestamp(timestamp_str)
        
        # Map user fields
        alert.user_name = record.get('User Name (BNAME)', '') or record.get('Unnamed: 4', '')
        alert.full_name = record.get('Full Name (NAME_TEXT)', '') or record.get('Unnamed: 1', '')
        alert.client = record.get('Client (MANDT)', '') or record.get('Unnamed: 3', '')
        alert.application_server = record.get('Application Server (RFCDEST)', '') or record.get('Unnamed: 2', '')
        
        # Duration
        duration_str = record.get('Duration In Time Units (DURATION)', '') or record.get('Unnamed: 9', '')
        if duration_str:
            try:
                alert.duration = int(float(str(duration_str)))
            except:
                pass
        
        alert.duration_unit = record.get('Duration Unit (DURATION_UNIT)', '') or record.get('Unnamed: 10', '')
        
        # IP and other fields
        alert.ip_address = record.get('IP address (HOSTADR)', '') or record.get('Unnamed: 12', '')
        alert.transaction_code = record.get('Transaction Code (TCODE)', '') or record.get('Unnamed: 6', '')
        
        # Date
        date_str = record.get('Date (DATE)', '') or record.get('Unnamed: 21', '')
        if date_str:
            alert.date = self._parse_date(date_str)
        
        return alert
    
    def _parse_soda_record(self, record: Dict[str, Any], report_type: str) -> SoDAReport:
        """Parse a single SoDA report record"""
        report = SoDAReport()
        
        # Extract common fields (varies by report type)
        # Try common field names
        report.user_name = (
            record.get('User Name', '') or
            record.get('User', '') or
            record.get('BNAME', '') or
            record.get(list(record.keys())[0] if record else '', '')
        )
        
        report.role_name = (
            record.get('Role Name', '') or
            record.get('Role', '') or
            record.get('ROLE', '')
        )
        
        report.transaction_code = (
            record.get('Transaction Code', '') or
            record.get('TCODE', '') or
            record.get('Transaction', '')
        )
        
        report.authorization_object = (
            record.get('Authorization Object', '') or
            record.get('AUTH_OBJECT', '')
        )
        
        # Set violation type based on report type
        if 'VIOLATION' in report_type or 'AVR' in report_type or 'PVR' in report_type:
            report.violation_type = "SoD Violation"
            report.risk_level = "High"
        elif 'FRAUD' in str(record).upper():
            report.violation_type = "Fraud Indicator"
            report.risk_level = "Critical"
        else:
            report.violation_type = "Access Issue"
            report.risk_level = "Medium"
        
        return report
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string"""
        if not timestamp_str:
            return datetime.utcnow()
        
        # Try common formats
        formats = [
            "%d.%m.%Y, %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(timestamp_str), fmt)
            except:
                continue
        
        return datetime.utcnow()
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string"""
        if not date_str:
            return None
        
        formats = [
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d.%m.%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except:
                continue
        
        return None

