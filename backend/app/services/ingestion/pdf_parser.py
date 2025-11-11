import pdfplumber
from pathlib import Path
from typing import Dict, Any, List
from .base_parser import BaseParser


class PDFParser(BaseParser):
    """Parser for PDF files"""
    
    def can_parse(self, file_path: str) -> bool:
        return self.get_file_extension(file_path) == 'pdf'
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF file"""
        result = {
            'metadata': {},
            'data': [],
            'errors': []
        }
        
        try:
            with pdfplumber.open(file_path) as pdf:
                # Extract metadata
                metadata = pdf.metadata or {}
                
                # Extract text from all pages
                full_text = []
                tables = []
                
                for page in pdf.pages:
                    # Extract text
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
                    
                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)
                
                result['metadata'] = {
                    'page_count': len(pdf.pages),
                    'title': metadata.get('Title', ''),
                    'author': metadata.get('Author', ''),
                    'subject': metadata.get('Subject', ''),
                }
                
                result['data'] = {
                    'text': '\n\n'.join(full_text),
                    'tables': tables
                }
                
        except Exception as e:
            result['errors'].append(f"Error parsing PDF: {str(e)}")
        
        return result

