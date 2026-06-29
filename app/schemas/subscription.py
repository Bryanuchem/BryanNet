from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SubscriptionStatus(str, Enum):
    QUEUED = "queued"
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class SubscriptionPurchase(BaseModel):
    customer_id: int
    plan_id: int


class SubscriptionResponse(BaseModel):
    subscription_id: int
    customer_id: int
    plan_id: int
    start_date: datetime
    expiry_date: datetime
    activation_sequence: int
    status: SubscriptionStatus

    class Config:
        from_attributes = True


class SubscriptionStatusResponse(BaseModel):
    plan_name: str | None = None
    status: SubscriptionStatus | None = None
    expiry_date: str | None = None
    queued_subscriptions: int


# ==========================================================
# Admin Dashboard Schemas
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

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = None
    start_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    activation_sequence: Optional[int] = None


class SubscriptionStatusUpdate(BaseModel):
    status: SubscriptionStatus