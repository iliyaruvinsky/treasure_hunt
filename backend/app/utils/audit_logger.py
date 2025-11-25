"""
Audit logging utility for tracking user actions
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def audit_log(
    db: Session,
    action: str,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    user_id: Optional[str] = None,
    user_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    description: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    status: str = "success",
    error_message: Optional[str] = None
):
    """
    Create an audit log entry
    
    Args:
        db: Database session
        action: Action performed (upload, delete, analyze, etc.)
        entity_type: Type of entity affected (data_source, finding, etc.)
        entity_id: ID of the affected entity
        user_id: User identifier (if available)
        user_ip: User IP address
        user_agent: User agent string
        description: Human-readable description
        details: Additional structured data
        status: success, error, or partial
        error_message: Error message if status is error
    """
    try:
        log_entry = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            user_ip=user_ip,
            user_agent=user_agent,
            description=description,
            details=details,
            status=status,
            error_message=error_message
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        # Don't fail the main operation if logging fails
        db.rollback()
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to create audit log: {str(e)}")

