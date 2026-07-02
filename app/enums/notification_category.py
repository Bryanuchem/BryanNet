from enum import Enum


class NotificationCategory(
    str,
    Enum,
):

    CUSTOMER = "customer"

    ADMIN = "admin"

    SYSTEM = "system"