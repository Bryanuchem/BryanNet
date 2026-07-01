from pydantic import BaseModel


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
    role: str
    is_active: bool