import pandas as pd
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_parser import BaseParser


class ExcelParserSoDA(BaseParser):
    """Parser for Skywind SoDA Excel report files"""
    
    # SoDA report type patterns
    REPORT_TYPES = {
        'AVR': 'Access Violation Review',
        'PVR': 'Potential Violation Review',
        'ARP': 'Access Review Process',
        'CRV': 'Custom Role Violation',
        'IVR': 'Initial Violation Review',
        'RAU': 'Role Access Update',
        'TRU': 'Transaction Role Update',
        'UAT': 'User Access Test',
    }
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file is a Skywind SoDA Excel file"""
        if not self.get_file_extension(file_path) == 'xlsx':
            return False
        
        filename = Path(file_path).stem
        
        # Check for SoDA report type patterns
        for report_type in self.REPORT_TYPES.keys():
            if filename.startswith(report_type) or f'_{report_type}_' in filename:
                return True
        
        # Check for special report names
        special_reports = [
            'Completely_Empty_Roles',
            'Roles_with_0_T-Codes',
            'Roles_with_0_users'
        ]
        for special in special_reports:
            if special in filename:
                return True
        
        # Check if file has "Parameters" and "KPIs" sheets (SoDA structure)
        try:
            xl_file = pd.ExcelFile(file_path)
            if 'Parameters' in xl_file.sheet_names and 'KPIs' in xl_file.sheet_names:
                return True
        except Exception:
            pass
        
        return False
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse Skywind SoDA Excel file"""
        result = {
            'metadata': {},
            'data': [],
            'errors': []
        }
        
        try:
            filename = Path(file_path).stem
            
            # Detect report type
            report_type = self._detect_report_type(filename)
            
            # Read all sheets
            xl_file = pd.ExcelFile(file_path)
            
            # Parse Parameters sheet
            parameters = {}
            if 'Parameters' in xl_file.sheet_names:
                try:
                    params_df = pd.read_excel(file_path, sheet_name='Parameters', header=0)
                    parameters = self._parse_parameters(params_df)
                except Exception as e:
                    result['errors'].append(f"Error parsing Parameters: {str(e)}")
            
            # Parse KPIs sheet
            kpis = {}
            if 'KPIs' in xl_file.sheet_names:
                try:
                    kpis_df = pd.read_excel(file_path, sheet_name='KPIs', header=0)
                    kpis = self._parse_kpis(kpis_df)
                except Exception as e:
                    result['errors'].append(f"Error parsing KPIs: {str(e)}")
            
            # Parse Result sheet(s)
            data_records = []
            result_sheets = [s for s in xl_file.sheet_names if s.startswith('Result')]
            
            for sheet_name in result_sheets:
                try:
                    # First row contains headers
                    result_df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
                    
                    # Skip the first row if it's just headers
                    if len(result_df) > 0:
                        # Use first row as column names
                        result_df.columns = result_df.iloc[0]
                        result_df = result_df[1:].reset_index(drop=True)
                    
                    # Convert to records
                    records = result_df.to_dict('records')
                    data_records.extend(records)
                except Exception as e:
                    result['errors'].append(f"Error parsing {sheet_name}: {str(e)}")
            
            # Extract report date from filename if available
            report_date = self._extract_date_from_filename(filename)
            
            # Build metadata
            result['metadata'] = {
                'report_type': report_type,
                'report_type_name': self.REPORT_TYPES.get(report_type, 'Unknown'),
                'filename': filename,
                'parameters': parameters,
                'kpis': kpis,
                'data_row_count': len(data_records),
                'report_date': report_date.isoformat() if report_date else None,
                'sheets': xl_file.sheet_names
            }
            
            result['data'] = data_records
            
        except Exception as e:
            result['errors'].append(f"Error parsing file: {str(e)}")
        
        return result
    
    def _detect_report_type(self, filename: str) -> str:
        """Detect SoDA report type from filename"""
        # Check for report type codes
        for report_type in self.REPORT_TYPES.keys():
            if filename.startswith(report_type) or f'_{report_type}_' in filename:
                return report_type
        
        # Check for special reports
        if 'Completely_Empty_Roles' in filename:
            return 'EMPTY_ROLES'
        if 'Roles_with_0_T-Codes' in filename:
            return 'ROLES_NO_TCODES'
        if 'Roles_with_0_users' in filename:
            return 'ROLES_NO_USERS'
        
        return 'UNKNOWN'
    
    def _parse_parameters(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse Parameters sheet"""
        params = {}
        
        try:
            for idx, row in df.iterrows():
                if len(row) >= 2 and pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]):
                    key = str(row.iloc[0]).strip()
                    value = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else None
                    if key:
                        params[key] = value
        except Exception:
            pass
        
        return params
    
    def _parse_kpis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse KPIs sheet"""
        kpis = {}
        
        try:
            for idx, row in df.iterrows():
                if len(row) >= 3 and pd.notna(row.iloc[0]):
                    metric = str(row.iloc[0]).strip()
                    value = row.iloc[1] if pd.notna(row.iloc[1]) else None
                    unit = row.iloc[2] if len(row) > 2 and pd.notna(row.iloc[2]) else None
                    if metric:
                        kpis[metric] = {
                            'value': value,
                            'unit': unit
                        }
        except Exception:
            pass
        
        return kpis
    
    def _extract_date_from_filename(self, filename: str) -> Optional[datetime]:
        """Extract date from filename (format: DD.MM.YY)"""
        # Look for date pattern DD.MM.YY or DD.MM.YYYY
        date_pattern = r'(\d{2})\.(\d{2})\.(\d{2,4})'
        match = re.search(date_pattern, filename)
        
        if match:
            day, month, year = match.groups()
            year = int(year)
            if year < 100:
                year += 2000  # Assume 20XX
            try:
                return datetime(int(year), int(month), int(day))
            except ValueError:
                pass
        
        return None

