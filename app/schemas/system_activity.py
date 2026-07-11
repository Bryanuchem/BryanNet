from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.enums.audit_result import AuditResult

from app.schemas.pagination import (
    PaginatedResponse,
)

class SystemActivityResponse(BaseModel):

    audit_log_id: int

    action: str

    entity_type: str

    entity_id: int | None

    target_name: str | None

    result: AuditResult

    description: str

    old_values: dict[str, Any] | None

    new_values: dict[str, Any] | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )