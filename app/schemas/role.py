from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)


# ==========================================================
# Query Schemas
# ==========================================================

class RoleResponse(BaseModel):

    role_id: int

    role_name: str

    description: str | None

    is_system_role: bool

    is_active: bool

    assigned_users: int = 0

    permission_count: int = 0

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

# ==========================================================
# Create
# ==========================================================

class CreateRoleRequest(BaseModel):

    role_name: str

    description: str | None = None

    is_system_role: bool = False


# ==========================================================
# Update
# ==========================================================

class UpdateRoleRequest(BaseModel):

    role_name: str

    description: str | None = None


# ==========================================================
# Activation
# ==========================================================

class RoleActivationRequest(BaseModel):

    is_active: bool
    
    
# ==========================================================
# Delete
# ==========================================================

class DeleteRoleResponse(BaseModel):

    message: str