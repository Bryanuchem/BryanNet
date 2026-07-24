from app.enums import (
    PortalAuthenticationError,
)


class PortalAuthenticationMessageService:
    """
    Maps authentication business errors
    to user-friendly messages.

    This class contains no business logic.
    It simply translates authentication
    errors into display messages.
    """

    _MESSAGES = {

        # ======================================================
        # Credentials
        # ======================================================

        PortalAuthenticationError.INVALID_USERNAME: (
            "Invalid username or password."
        ),

        PortalAuthenticationError.INVALID_PASSWORD: (
            "Invalid username or password."
        ),

        # ======================================================
        # Customer
        # ======================================================

        PortalAuthenticationError.CUSTOMER_NOT_FOUND: (
            "Customer account not found."
        ),

        PortalAuthenticationError.CUSTOMER_DISABLED: (
            "Your account has been disabled. Please contact support."
        ),

        # ======================================================
        # Subscription
        # ======================================================

        PortalAuthenticationError.NO_ACTIVE_SUBSCRIPTION: (
            "You do not have an active subscription."
        ),

        PortalAuthenticationError.SUBSCRIPTION_EXPIRED: (
            "Your subscription has expired."
        ),

        # ======================================================
        # Plan
        # ======================================================

        PortalAuthenticationError.PLAN_INACTIVE: (
            "Your subscription plan is currently unavailable."
        ),

        PortalAuthenticationError.PLAN_EXPIRED: (
            "Your subscription plan has expired."
        ),

        # ======================================================
        # Router Account
        # ======================================================

        PortalAuthenticationError.ROUTER_ACCOUNT_NOT_FOUND: (
            "Invalid username or password.",
        ),

        PortalAuthenticationError.ROUTER_ACCOUNT_DISABLED: (
            "Your internet account has been disabled."
        ),

        # ======================================================
        # Device
        # ======================================================

        PortalAuthenticationError.DEVICE_NOT_FOUND: (
            "This device is not registered. Please contact support."
        ),

        PortalAuthenticationError.DEVICE_INACTIVE: (
            "This device is inactive."
        ),

        PortalAuthenticationError.DEVICE_BLOCKED: (
            "This device has been blocked. Please contact support."
        ),

        PortalAuthenticationError.DEVICE_OWNERSHIP_MISMATCH: (
            "This device belongs to another customer."
        ),

        PortalAuthenticationError.CONCURRENT_DEVICE_LIMIT_REACHED: (
            "You have reached the maximum number of devices that can be connected at the same time."
        ),

        PortalAuthenticationError.REGISTERED_DEVICE_LIMIT_REACHED: (
            "You have reached the maximum number of registered devices allowed on your plan. Please remove an existing device or contact support."
        ),

        # ======================================================
        # System
        # ======================================================

        PortalAuthenticationError.UNKNOWN_ERROR: (
            "Authentication failed. Please try again. If the problem persists, please contact support."
        ),

    }

    @classmethod
    def get_message(
        cls,
        error: PortalAuthenticationError | None,
    ) -> str:

        if error is None:

            return cls._MESSAGES[
                PortalAuthenticationError.UNKNOWN_ERROR
            ]

        return cls._MESSAGES.get(

            error,

            cls._MESSAGES[
                PortalAuthenticationError.UNKNOWN_ERROR
            ],

        )