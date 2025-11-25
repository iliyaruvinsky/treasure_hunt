import pandas as pd
from pathlib import Path
from typing import Dict, Any
from .base_parser import BaseParser


class CSVParser(BaseParser):
    """Parser for CSV files"""
    
    def can_parse(self, file_path: str) -> bool:
        return self.get_file_extension(file_path) == 'csv'
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV file"""
        result = {
            'metadata': {},
            'data': [],
            'errors': []
        }
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                result['errors'].append("Could not decode CSV file with any standard encoding")
                return result
            
            # Convert to records, handling NaN values
            df = df.where(pd.notna(df), None)
            records = df.to_dict('records')
            
            result['metadata'] = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': df.columns.tolist()
            }
            
            result['data'] = records
            
        except Exception as e:
            result['errors'].append(f"Error parsing CSV: {str(e)}")
        
        return result

