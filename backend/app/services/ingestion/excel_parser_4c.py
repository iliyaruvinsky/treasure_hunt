import pandas as pd
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from .base_parser import BaseParser


class ExcelParser4C(BaseParser):
    """Parser for Skywind 4C Excel alert files"""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if file is a Skywind 4C Excel file"""
        if not self.get_file_extension(file_path) == 'xlsx':
            return False
        
        # Check filename pattern for 4C alerts (SLG_XXXXXX_XXXXXX)
        filename = Path(file_path).stem
        if re.search(r'SLG_\d{6}_\d{6}', filename):
            return True
        
        # Check if file has "Alert Parameters" sheet
        try:
            xl_file = pd.ExcelFile(file_path)
            if 'Alert Parameters' in xl_file.sheet_names:
                return True
        except Exception:
            pass
        
        return False
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse Skywind 4C Excel file"""
        result = {
            'metadata': {},
            'data': [],
            'errors': []
        }
        
        try:
            # Extract alert ID from filename
            filename = Path(file_path).stem
            alert_id_match = re.search(r'SLG_(\d{6}_\d{6})', filename)
            alert_id = alert_id_match.group(0) if alert_id_match else None
            
            # Extract alert name from filename
            alert_name = self._extract_alert_name(filename)
            
            # Read all sheets
            xl_file = pd.ExcelFile(file_path)
            
            # Parse Alert Parameters sheet
            alert_params = {}
            if 'Alert Parameters' in xl_file.sheet_names:
                try:
                    params_df = pd.read_excel(file_path, sheet_name='Alert Parameters', header=0)
                    alert_params = self._parse_alert_parameters(params_df)
                except Exception as e:
                    result['errors'].append(f"Error parsing Alert Parameters: {str(e)}")
            
            # Parse Data sheet
            data_records = []
            if 'Data' in xl_file.sheet_names:
                try:
                    # First row contains actual headers
                    data_df = pd.read_excel(file_path, sheet_name='Data', header=0)
                    
                    # Skip the first row if it's just headers
                    if len(data_df) > 0:
                        # Use first row as column names
                        data_df.columns = data_df.iloc[0]
                        data_df = data_df[1:].reset_index(drop=True)
                    
                    # Convert to records
                    data_records = data_df.to_dict('records')
                except Exception as e:
                    result['errors'].append(f"Error parsing Data sheet: {str(e)}")
            
            # Build metadata
            result['metadata'] = {
                'alert_id': alert_id,
                'alert_name': alert_name,
                'filename': filename,
                'parameters': alert_params,
                'data_row_count': len(data_records),
                'sheets': xl_file.sheet_names
            }
            
            result['data'] = data_records
            
        except Exception as e:
            result['errors'].append(f"Error parsing file: {str(e)}")
        
        return result
    
    def _extract_alert_name(self, filename: str) -> str:
        """Extract alert name from filename"""
        # Remove common prefixes and suffixes
        name = filename.replace('Summary_', '').replace('_SLG_', ' SLG_')
        
        # Remove alert ID pattern
        name = re.sub(r'SLG_\d{6}_\d{6}', '', name).strip()
        
        # Remove file extensions and version info
        name = re.sub(r'\.xlsx$', '', name, flags=re.IGNORECASE)
        
        return name
    
    def _parse_alert_parameters(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse Alert Parameters sheet into structured format"""
        params = {
            'layers': [],
            'filters': []
        }
        
        try:
            # Skip header row if present
            if len(df) > 0:
                for idx, row in df.iterrows():
                    if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip():
                        layer = {
                            'layer': row.iloc[0] if pd.notna(row.iloc[0]) else None,
                            'field': row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else None,
                            'description': row.iloc[2] if len(row) > 2 and pd.notna(row.iloc[2]) else None,
                            'type': row.iloc[3] if len(row) > 3 and pd.notna(row.iloc[3]) else None,
                            'condition': row.iloc[4] if len(row) > 4 and pd.notna(row.iloc[4]) else None,
                            'from_value': row.iloc[5] if len(row) > 5 and pd.notna(row.iloc[5]) else None,
                            'to_value': row.iloc[6] if len(row) > 6 and pd.notna(row.iloc[6]) else None,
                        }
                        if layer['field']:
                            params['layers'].append(layer)
        except Exception as e:
            pass
        
        return params

