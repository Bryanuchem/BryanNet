from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.enums import (
    PaymentStatus,
)

from app.schemas.types import (
    PositiveInt,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PortalPaymentCreate(BaseModel):

    telegram_user_id: int

    plan_id: PositiveInt


# ==========================================================
# Response Schemas
# ==========================================================

class PortalPaymentResponse(BaseModel):

    payment_reference: str

    plan_name: str

    amount: Decimal

    status: PaymentStatus

    checkout_url: str | None = None
    
    subscription_queued: bool = False

    payment_date: datetime | None

    created_at: datetime

    class Config:

        from_attributes = True
        
class PortalPaymentDetailResponse(
    PortalPaymentResponse,
):

    payment_provider: str

    payment_channel: str

    gateway_reference: str | None

    gateway_transaction_id: str | None

    authorization_code: str | None

    gateway_status: str | None

    paid_at: datetime | None