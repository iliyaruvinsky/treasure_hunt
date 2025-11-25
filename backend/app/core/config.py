from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "openai"  # openai or anthropic
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # File Storage
    STORAGE_TYPE: str = "local"  # local or s3
    STORAGE_PATH: str = "./storage"
    
    # Data Ingestion Limits
    MAX_RECORDS_PER_FILE: Optional[int] = None  # None = no limit, set to limit records per file
    BATCH_SIZE: int = 1000  # Process records in batches to avoid memory issues
    
    # Application
    SECRET_KEY: str
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Treasure Hunt Analyzer"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

