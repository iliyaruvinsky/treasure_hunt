"""
Service to save parsed data to database
"""
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime
import re

from app.models.data_source import DataSource
from app.models.alert import Alert, AlertMetadata
from app.models.soda_report import SoDAReport, SoDAReportMetadata


class DataSaver:
    """Save parsed data to database"""
    
    def __init__(self, db: Session):
        self.db = db
    
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
        for record in data[:1000]:  # Limit to first 1000 records for initial testing
            alert = self._parse_alert_record(record)
            alert.data_source_id = data_source.id
            alert.raw_data = record
            self.db.add(alert)
        
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
        for record in data[:1000]:  # Limit to first 1000 records
            report = self._parse_soda_record(record, metadata.get('report_type'))
            report.data_source_id = data_source.id
            report.raw_data = record
            self.db.add(report)
        
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

