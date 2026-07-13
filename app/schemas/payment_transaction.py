from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.enums import (
    PaymentProvider,
    TransactionStatus,
)


# ==========================================================
# Request Schemas
# ==========================================================

class PaymentTransactionCreate(BaseModel):

    payment_id: int

    payment_provider: PaymentProvider


class PaymentTransactionUpdate(BaseModel):

    transaction_status: TransactionStatus | None = None

    gateway_reference: str | None = None

    gateway_transaction_id: str | None = None

    gateway_status: str | None = None

    authorization_code: str | None = None

    gateway_response: str | None = None

    metadata: dict[str, Any] | None = None

    paid_at: datetime | None = None

    webhook_received_at: datetime | None = None


# ==========================================================
# Response Schemas
# ==========================================================

class PaymentTransactionResponse(BaseModel):

    transaction_id: int

    payment_id: int

    payment_provider: PaymentProvider

    transaction_status: TransactionStatus

    gateway_reference: str | None

    gateway_transaction_id: str | None

    gateway_status: str | None

    authorization_code: str | None

    currency: str

    gateway_response: str | None

    metadata: dict[str, Any] | None

    paid_at: datetime | None

    webhook_received_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True