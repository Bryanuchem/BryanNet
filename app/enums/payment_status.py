from enum import Enum


class PaymentStatus(str, Enum):

    PENDING = "pending"

    SUCCESSFUL = "successful"

    FAILED = "failed"

    CANCELLED = "cancelled"

    REFUNDED = "refunded"