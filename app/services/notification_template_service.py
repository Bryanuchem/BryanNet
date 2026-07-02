from datetime import datetime


class NotificationTemplateService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _format_date(
        value,
    ):

        if value is None:

            return "N/A"

        if isinstance(
            value,
            datetime,
        ):

            return value.strftime(
                "%d %b %Y %I:%M %p"
            )

        return str(value)

    # ==========================================================
    # Customer Templates
    # ==========================================================

    @staticmethod
    def welcome(
        customer,
    ):

        return (

            "🎉 Welcome to BryanNet!\n\n"

            f"Hello {customer.full_name},\n\n"

            "Your account has been created "
            "successfully.\n"

            "Thank you for choosing BryanNet."

        )

    @staticmethod
    def payment_success(
        payment,
    ):

        return (

            "✅ Payment Successful\n\n"

            f"We have received your payment "
            f"of ₦{payment.amount}.\n\n"

            f"Reference: "
            f"{payment.payment_reference}"

        )

    @staticmethod
    def payment_failed(
        payment,
    ):

        return (

            "❌ Payment Failed\n\n"

            "Unfortunately, your payment "
            "could not be processed.\n\n"

            f"Reference: "
            f"{payment.payment_reference}"

        )

    @staticmethod
    def subscription_created(
        subscription,
    ):

        return (

            "🎉 Subscription Activated\n\n"

            "Your subscription is now active.\n\n"

            f"Expiry Date: "

            f"{NotificationTemplateService._format_date(subscription.expiry_date)}"

        )

    @staticmethod
    def subscription_expiring(
        subscription,
        days_remaining,
    ):

        return (

            "📅 Subscription Expiring\n\n"

            f"Your subscription will expire "
            f"in {days_remaining} day(s).\n\n"

            "Please renew to avoid service "
            "interruption.\n\n"

            f"Expiry Date: "

            f"{NotificationTemplateService._format_date(subscription.expiry_date)}"

        )

    @staticmethod
    def subscription_expired(
        subscription,
    ):

        return (

            "⛔ Subscription Expired\n\n"

            "Your subscription has expired.\n\n"

            "Please renew your subscription "
            "to restore Internet access.\n\n"

            f"Expired On: "

            f"{NotificationTemplateService._format_date(subscription.expiry_date)}"

        )

    @staticmethod
    def device_registered(
        device,
    ):

        return (

            "📱 Device Registered\n\n"

            f"Device: "
            f"{device.device_name}\n"

            f"MAC Address: "
            f"{device.mac_address}\n\n"

            "The device has been successfully "
            "linked to your account."

        )

    @staticmethod
    def device_blocked(
        device,
    ):

        return (

            "🚫 Device Blocked\n\n"

            f"Device: "
            f"{device.device_name}\n"

            f"MAC Address: "
            f"{device.mac_address}\n\n"

            "This device can no longer "
            "access your subscription."

        )
        
    # ==========================================================
    # Admin Templates
    # ==========================================================

    @staticmethod
    def router_offline(
        router,
    ):

        return (

            "📡 Router Offline\n\n"

            f"Router: "
            f"{router.router_name}\n"

            f"IP Address: "
            f"{router.ip_address}\n\n"

            "The router is currently "
            "unreachable.\n"

            "Immediate attention is "
            "recommended."

        )

    @staticmethod
    def router_online(
        router,
    ):

        return (

            "✅ Router Online\n\n"

            f"Router: "
            f"{router.router_name}\n"

            f"IP Address: "
            f"{router.ip_address}\n\n"

            "The router has returned "
            "to normal operation."

        )

    # ==========================================================
    # System Templates
    # ==========================================================

    @staticmethod
    def system_message(
        subject,
        message,
    ):

        return (

            "⚙️ System Notification\n\n"

            f"{subject}\n\n"

            f"{message}"

        )        