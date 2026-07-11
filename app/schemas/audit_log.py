from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.enums.audit_result import AuditResult


# ==========================================================
# Query Schemas
# ==========================================================

class AuditLogResponse(BaseModel):

    audit_log_id: int

    admin_id: int | None
    
    administrator: str | None

    admin_session_id: int | None

    action: str

    entity_type: str

    entity_id: int | None

    target_name: str | None

    result: AuditResult

    description: str

    old_values: dict[str, Any] | None

    new_values: dict[str, Any] | None

    ip_address: str | None

    user_agent: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )