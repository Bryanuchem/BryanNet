from enum import Enum


class NotificationPriority(
    str,
    Enum,
):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    CRITICAL = "critical"