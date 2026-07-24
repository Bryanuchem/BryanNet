from enum import (
    Enum,
)


class PortalAuthenticationError(
    str,
    Enum,
):

    # ==========================================================
    # Credentials
    # ==========================================================

    INVALID_USERNAME = "INVALID_USERNAME"

    INVALID_PASSWORD = "INVALID_PASSWORD"

    # ==========================================================
    # Customer
    # ==========================================================

    CUSTOMER_NOT_FOUND = "CUSTOMER_NOT_FOUND"

    CUSTOMER_DISABLED = "CUSTOMER_DISABLED"

    # ==========================================================
    # Subscription
    # ==========================================================

    NO_ACTIVE_SUBSCRIPTION = "NO_ACTIVE_SUBSCRIPTION"

    SUBSCRIPTION_EXPIRED = "SUBSCRIPTION_EXPIRED"

    # ==========================================================
    # Plan
    # ==========================================================

    PLAN_INACTIVE = "PLAN_INACTIVE"

    PLAN_EXPIRED = "PLAN_EXPIRED"

    # ==========================================================
    # Router Account
    # ==========================================================

    ROUTER_ACCOUNT_NOT_FOUND = "ROUTER_ACCOUNT_NOT_FOUND"

    ROUTER_ACCOUNT_DISABLED = "ROUTER_ACCOUNT_DISABLED"

    # ==========================================================
    # Device
    # ==========================================================

    DEVICE_NOT_FOUND = "DEVICE_NOT_FOUND"

    DEVICE_INACTIVE = "DEVICE_INACTIVE"

    DEVICE_BLOCKED = "DEVICE_BLOCKED"

    DEVICE_OWNERSHIP_MISMATCH = "DEVICE_OWNERSHIP_MISMATCH"

    CONCURRENT_DEVICE_LIMIT_REACHED = "CONCURRENT_DEVICE_LIMIT_REACHED"


    REGISTERED_DEVICE_LIMIT_REACHED = "REGISTERED_DEVICE_LIMIT_REACHED"
    
    # ==========================================================
    # System
    # ==========================================================

    UNKNOWN_ERROR = "UNKNOWN_ERROR"