from enum import Enum


class PendingLoginStatus(str, Enum):

    PENDING = "pending"

    CONSUMED = "consumed"

    EXPIRED = "expired"