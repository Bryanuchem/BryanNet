from enum import Enum


class SubscriptionStatus(str, Enum):

    QUEUED = "queued"

    ACTIVE = "active"

    EXPIRED = "expired"

    CANCELLED = "cancelled"