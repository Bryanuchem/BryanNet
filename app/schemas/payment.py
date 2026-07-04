from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.enums import (
    PaymentProvider,
    PaymentStatus,
    PaymentChannel,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PaymentCreate(BaseModel):

    customer_id: int

    plan_id: int

    payment_provider: PaymentProvider

    payment_channel: PaymentChannel

    payment_method: str


class PaymentFilter(BaseModel):

    search: str | None = None

    payment_provider: PaymentProvider | None = None

    status: PaymentStatus | None = None


# ==========================================================
# Response Schemas
# ==========================================================

class PaymentResponse(BaseModel):

    payment_reference: str

    customer_id: int

    plan_id: int

    subscription_id: int | None

    amount: Decimal

    payment_provider: PaymentProvider

    payment_method: str | None

    gateway_transaction_id: str | None

    status: PaymentStatus

    payment_date: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True


class PaymentListItem(BaseModel):

    payment_reference: str

    customer_id: int

    customer_name: str

    plan_id: int

    plan_name: str

    amount: Decimal

    payment_provider: PaymentProvider

    payment_channel: PaymentChannel

    payment_method: str | None

    status: PaymentStatus

    payment_date: datetime | None

    created_at: datetime

    class Config:

        from_attributes = True

class PaymentStatsResponse(BaseModel):

    total_payments: int

    pending_payments: int

    successful_payments: int

    failed_payments: int

    cancelled_payments: int

    refunded_payments: int

    expired_payments: int

    total_revenue: Decimal