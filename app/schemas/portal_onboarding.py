from pydantic import BaseModel

from app.schemas.types import (
    FullName,
    PhoneNumber,
    PositiveInt,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PortalOnboardingStart(BaseModel):

    telegram_user_id: PositiveInt


class PortalUpdateName(BaseModel):

    telegram_user_id: PositiveInt

    full_name: FullName


class PortalUpdatePhone(BaseModel):

    telegram_user_id: PositiveInt

    phone_number: PhoneNumber


# ==========================================================
# Response Schemas
# ==========================================================

class PortalOnboardingResponse(BaseModel):

    customer_id: int

    telegram_user_id: int | None = None

    full_name: str | None = None

    phone_number: str | None = None

    is_registered: bool

    status: str

    registration_step: str

    class Config:

        from_attributes = True