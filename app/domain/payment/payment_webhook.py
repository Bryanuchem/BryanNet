from dataclasses import (
    dataclass,
)

from app.enums import (
    PaymentProvider,
)

from .payment_result import (
    PaymentResult,
)


@dataclass(
    slots=True,
)
class PaymentWebhookResult(
    PaymentResult,
):

    valid: bool = False

    provider: PaymentProvider | None = None

    event: str | None = None

    gateway_reference: str | None = None