from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


# ==========================================================
# Query Schemas
# ==========================================================

class AdminUserResponse(BaseModel):

    admin_user_id: int

    username: str

    email: EmailStr

    role_id: int

    role_name: str
    
    permissions: list[str]

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# Create
# ==========================================================

class CreateAdminUserRequest(BaseModel):

    username: str

    email: EmailStr

    password: str

    role_id: int


# ==========================================================
# Update
# ==========================================================

class UpdateAdminUserRequest(BaseModel):

    username: str

    email: EmailStr


# ==========================================================
# Change Password
# ==========================================================

class ChangePasswordRequest(BaseModel):

    password: str


# ==========================================================
# Change Role
# ==========================================================

class ChangeRoleRequest(BaseModel):

    role_id: int


# ==========================================================
# Activation
# ==========================================================

class AdminUserActivationRequest(BaseModel):

    is_active: bool