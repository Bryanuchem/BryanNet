from enum import Enum


class TransactionStatus(
    str,
    Enum,
):

    PENDING = "PENDING"

    SUCCESSFUL = "SUCCESSFUL"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"

    EXPIRED = "EXPIRED"

    ABANDONED = "ABANDONED"