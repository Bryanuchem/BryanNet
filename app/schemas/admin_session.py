from datetime import datetime

from pydantic import BaseModel

from app.enums import (
    LoginSource,
    LogoutReason,
)

class AdminSessionResponse(BaseModel):

    admin_session_id: int

    admin_user_id: int

    login_time: datetime

    last_activity: datetime

    logout_time: datetime | None

    ip_address: str | None

    user_agent: str | None

    login_source: LoginSource

    client_name: str

    logout_reason: LogoutReason | None

    is_active: bool

    class Config:

        from_attributes = True