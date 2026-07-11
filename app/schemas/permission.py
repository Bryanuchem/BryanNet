from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


# ==========================================================
# Query Schemas
# ==========================================================

class PermissionResponse(BaseModel):

    permission_id: int

    permission_key: str

    module: str

    action: str

    description: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class RolePermissionResponse(BaseModel):

    role_id: int

    permission_id: int

    permission_key: str

    module: str

    action: str

    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Command Schemas
# ==========================================================

class UpdateRolePermissionsRequest(BaseModel):

    permission_ids: list[int]