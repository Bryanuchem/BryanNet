from dataclasses import (
    dataclass,
)

from .payment_result import (
    PaymentResult,
)


@dataclass(
    slots=True,
)
class PaymentInitializationResult(
    PaymentResult,
):

    authorization_url: str | None = None

    access_code: str | None = None

    gateway_reference: str | None = None

    gateway_status: str | None = None

    gateway_response: str | None = None