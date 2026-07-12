from datetime import datetime

from pydantic import BaseModel

from app.enums import (
    SubscriptionStatus,
)

from app.schemas.types import (
    PositiveInt,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PortalSubscriptionPurchase(BaseModel):

    telegram_user_id: int

    plan_id: PositiveInt


class PortalSubscriptionActionRequest(BaseModel):

    telegram_user_id: int


# ==========================================================
# Response Schemas
# ==========================================================

class PortalSubscriptionResponse(BaseModel):

    subscription_id: int

    plan_name: str

    price: float

    speed_limit_mbps: int

    max_devices: int

    concurrent_devices: int

    start_date: datetime

    expiry_date: datetime

    activated_at: datetime | None

    activation_sequence: int

    status: SubscriptionStatus

    queued_subscriptions: int

    remaining_days: int

    has_active_subscription: bool

    class Config:

        from_attributes = True