from typing import Optional
from pathlib import Path
from .base_parser import BaseParser
from .pdf_parser import PDFParser
from .csv_parser import CSVParser
from .docx_parser import DOCXParser
from .excel_parser_4c import ExcelParser4C
from .excel_parser_soda import ExcelParserSoDA


class ParserFactory:
    """Factory for creating appropriate parser based on file type"""
    
    _parsers = [
        ExcelParser4C(),  # Check 4C first (more specific)
        ExcelParserSoDA(),  # Check SoDA second (more specific)
        PDFParser(),
        CSVParser(),
        DOCXParser(),
    ]
    
    @classmethod
    def get_parser(cls, file_path: str) -> Optional[BaseParser]:
        """Get appropriate parser for the file"""
        for parser in cls._parsers:
            if parser.can_parse(file_path):
                return parser
        return None
    
    @classmethod
    def can_parse_file(cls, file_path: str) -> bool:
        """Check if any parser can handle this file"""
        parser = cls.get_parser(file_path)
        return parser is not None

