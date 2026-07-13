from dataclasses import (
    dataclass,
)

from datetime import datetime

from app.enums import (
    TransactionStatus,
)

from .payment_result import (
    PaymentResult,
)


@dataclass(
    slots=True,
)
class PaymentVerificationResult(
    PaymentResult,
):

    verified: bool = False

    transaction_status: (
        TransactionStatus | None
    ) = None

    gateway_reference: str | None = None

    gateway_transaction_id: str | None = None

    authorization_code: str | None = None

    paid_at: datetime | None = None

    gateway_status: str | None = None

    gateway_response: str | None = None