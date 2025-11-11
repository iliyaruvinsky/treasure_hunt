from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class FieldMapping(Base):
    __tablename__ = "field_mappings"

    id = Column(Integer, primary_key=True, index=True)
    source_system = Column(String, nullable=False)  # skywind_4c, skywind_soda
    source_field_name = Column(String, nullable=False)
    target_field_name = Column(String, nullable=False)  # Standardized field name
    field_type = Column(String)  # string, integer, datetime, etc.
    description = Column(Text)
    
    # Index for efficient lookups
    __table_args__ = (
        {"indexes": [
            {"name": "idx_source_field", "columns": ["source_system", "source_field_name"]}
        ]}
    )

