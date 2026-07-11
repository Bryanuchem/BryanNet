from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.enums import (
    LoginSource,
    LogoutReason,
)


# ==========================================================
# Query Schemas
# ==========================================================

class AdminSessionResponse(BaseModel):

    admin_session_id: int

    admin_user_id: int

    administrator: str

    login_time: datetime

    last_activity: datetime

    logout_time: datetime | None

    ip_address: str | None

    user_agent: str | None

    login_source: LoginSource

    client_name: str

    logout_reason: LogoutReason | None

    is_active: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )