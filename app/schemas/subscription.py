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

class SubscriptionPurchase(BaseModel):

    customer_id: PositiveInt

    plan_id: PositiveInt


class SubscriptionUpdate(BaseModel):

    plan_id: PositiveInt | None = None

    start_date: datetime | None = None

    expiry_date: datetime | None = None

    activation_sequence: PositiveInt | None = None


class SubscriptionStatusUpdate(BaseModel):

    status: SubscriptionStatus


# ==========================================================
# Telegram Bot Responses
# ==========================================================

class SubscriptionResponse(BaseModel):

    subscription_id: int

    customer_id: int

    plan_id: int

    start_date: datetime

    expiry_date: datetime

    activation_sequence: int

    status: SubscriptionStatus
    
    activated_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True


class SubscriptionStatusResponse(BaseModel):

    has_active_subscription: bool

    plan_name: str | None = None

    expiry_date: datetime | None = None

    queued_subscriptions: int


# ==========================================================
# Admin Dashboard Responses
# ==========================================================

class SubscriptionAdminResponse(BaseModel):

    subscription_id: int

    customer_id: int

    customer_name: str

    plan_id: int

    plan_name: str

    price: float

    start_date: datetime

    expiry_date: datetime

    remaining_days: int

    activation_sequence: int

    status: SubscriptionStatus

    activated_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True