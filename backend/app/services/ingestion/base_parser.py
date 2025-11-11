from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path


class BaseParser(ABC):
    """Base class for all file parsers"""
    
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a file and return structured data
        
        Returns:
            Dict with keys:
            - metadata: Dict with file metadata
            - data: List of records or DataFrame-like structure
            - errors: List of any errors encountered
        """
        pass
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file"""
        pass
    
    def get_file_extension(self, file_path: str) -> str:
        """Get file extension in lowercase"""
        return Path(file_path).suffix.lower().lstrip('.')
    
    def validate_file(self, file_path: str) -> bool:
        """Validate that file exists and is readable"""
        path = Path(file_path)
        return path.exists() and path.is_file()

