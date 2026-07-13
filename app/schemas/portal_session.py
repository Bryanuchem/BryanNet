from pydantic import BaseModel

from app.enums import (
    NextAction,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PortalSessionRegister(BaseModel):

    telegram_user_id: int

    phone_number: str


# ==========================================================
# Response Schemas
# ==========================================================

class PortalSessionResponse(BaseModel):

    is_registered: bool

    customer_id: int | None = None

    full_name: str | None = None

    telegram_user_id: int

    next_action: NextAction
    
    has_active_subscription: bool

    class Config:

        from_attributes = True