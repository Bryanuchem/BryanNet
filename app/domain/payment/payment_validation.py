from dataclasses import (
    dataclass,
)


@dataclass(
    slots=True,
)
class PaymentValidationResult:

    valid: bool = False

    message: str | None = None