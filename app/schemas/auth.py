from pydantic import BaseModel
from pydantic import EmailStr

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

    email: EmailStr

    role: str
    
    permissions: list[str]

    is_active: bool