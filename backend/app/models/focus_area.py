from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class FocusArea(Base):
    __tablename__ = "focus_areas"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Focus areas:
    # 1. BUSINESS_PROTECTION - Fraud detection, cybersecurity
    # 2. BUSINESS_CONTROL - Bottlenecks, process observability, anomalies
    # 3. ACCESS_GOVERNANCE - SoD, authorizations, user access reviews
    # 4. TECHNICAL_CONTROL - Infrastructure, communications, technical anomalies
    # 5. JOBS_CONTROL - Job performance, resource utilization, anomalies
    # 6. S4HANA_EXCELLENCE - Post go-live, migration safeguarding

