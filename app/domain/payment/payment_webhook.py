from dataclasses import (
    dataclass,
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

    event: str | None = None

    gateway_reference: str | None = None