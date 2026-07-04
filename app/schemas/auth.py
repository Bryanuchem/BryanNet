from pydantic import BaseModel

from app.schemas.types import (
    Password,
    Username,
)


class LoginRequest(BaseModel):

    username: Username

    password: Password


class LoginResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class CurrentAdminResponse(BaseModel):

    admin_user_id: int

    username: str

    email: str

    role: str

    is_active: bool