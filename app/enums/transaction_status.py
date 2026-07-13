from enum import Enum


class TransactionStatus(
    str,
    Enum,
):

    PENDING = "pending"

    SUCCESSFUL = "successful"

    FAILED = "failed"

    CANCELLED = "cancelled"

    EXPIRED = "expired"

    ABANDONED = "abandoned"