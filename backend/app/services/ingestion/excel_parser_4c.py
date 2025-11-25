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
        
        filename = Path(file_path).stem
        
        # Check filename pattern for 4C alerts:
        # 1. SLG_XXXXXX_XXXXXX pattern (strongest indicator)
        if re.search(r'SLG_\d{6}_\d{6}', filename):
            return True
        
        # 2. Pattern like _200025_001374 (numeric alert ID pattern)
        # This is a strong indicator of 4C alerts - accept it even if we can't verify sheets
        if re.search(r'_\d{6}_\d{6}', filename):
            # Try to verify with "Alert Parameters" sheet if possible
            try:
                xl_file = pd.ExcelFile(file_path)
                if 'Alert Parameters' in xl_file.sheet_names:
                    return True
                # Even without Alert Parameters sheet, if it has the pattern, it's likely 4C
                # Check if it has a "Data" sheet (common in 4C alerts)
                if 'Data' in xl_file.sheet_names:
                    return True
            except Exception:
                # If we can't open the file, but it has the pattern, assume it's 4C
                # The pattern _XXXXXX_XXXXXX is very specific to 4C alerts
                return True
        
        # 3. Check if file has "Alert Parameters" sheet (strongest indicator)
        try:
            xl_file = pd.ExcelFile(file_path)
            sheet_names = xl_file.sheet_names
            
            if 'Alert Parameters' in sheet_names:
                return True
            
            # Also check for "Data" sheet - common in 4C alerts even without Alert Parameters
            if 'Data' in sheet_names:
                # Make sure it's not a SoDA report (which has Parameters and KPIs)
                # SoDA reports typically have both Parameters and KPIs sheets
                has_soda_structure = 'Parameters' in sheet_names and 'KPIs' in sheet_names
                if not has_soda_structure:
                    return True
            
            # Additional check: files with "Summary_" prefix and "Data" sheet are likely 4C alerts
            if filename.startswith('Summary_') and 'Data' in sheet_names:
                # Exclude SoDA structure
                if not ('Parameters' in sheet_names and 'KPIs' in sheet_names):
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
            
            # Try SLG_XXXXXX_XXXXXX pattern first
            alert_id_match = re.search(r'SLG_(\d{6}_\d{6})', filename)
            if alert_id_match:
                alert_id = alert_id_match.group(0)
            else:
                # Try _XXXXXX_XXXXXX pattern (without SLG_ prefix)
                alert_id_match = re.search(r'_(\d{6}_\d{6})', filename)
                if alert_id_match:
                    # Add SLG_ prefix for consistency
                    alert_id = f"SLG_{alert_id_match.group(1)}"
                else:
                    alert_id = None
            
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
                    # Try reading with header=0 first (standard case)
                    data_df = pd.read_excel(file_path, sheet_name='Data', header=0)
                    
                    # Check if first row looks like headers (contains text, not all numeric)
                    # If first row is all text/strings, it's likely the header row
                    first_row_is_header = False
                    if len(data_df) > 0:
                        first_row = data_df.iloc[0]
                        # Check if first row has mostly string values (likely headers)
                        non_numeric_count = sum(1 for val in first_row if pd.notna(val) and isinstance(val, str) and not str(val).replace('.', '').replace('-', '').isdigit())
                        if non_numeric_count > len(first_row) * 0.5:  # More than 50% are strings
                            first_row_is_header = True
                    
                    if first_row_is_header and len(data_df) > 0:
                        # Use first row as column names
                        data_df.columns = data_df.iloc[0]
                        data_df = data_df[1:].reset_index(drop=True)
                    
                    # Convert to records, handling NaN values
                    # This preserves ALL fields from the source file (up to 100+ fields)
                    data_df = data_df.where(pd.notna(data_df), None)
                    data_records = data_df.to_dict('records')  # All columns preserved
                except Exception as e:
                    # Try alternative parsing if first attempt fails
                    try:
                        # Try reading without assuming header structure
                        data_df = pd.read_excel(file_path, sheet_name='Data', header=None)
                        if len(data_df) > 1:
                            # Use first row as headers
                            data_df.columns = data_df.iloc[0]
                            data_df = data_df[1:].reset_index(drop=True)
                            data_df = data_df.where(pd.notna(data_df), None)
                            data_records = data_df.to_dict('records')
                        else:
                            result['errors'].append(f"Data sheet is empty or has insufficient rows")
                    except Exception as e2:
                        result['errors'].append(f"Error parsing Data sheet: {str(e)}. Alternative parsing also failed: {str(e2)}")
            
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

