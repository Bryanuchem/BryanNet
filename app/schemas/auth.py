from pydantic import BaseModel

from app.enums.admin_role import AdminRole


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentAdminResponse(BaseModel):
    admin_user_id: int
    username: str
    email: str
    role: AdminRole
    is_active: bool