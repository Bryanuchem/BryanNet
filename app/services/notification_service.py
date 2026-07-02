from app.enums import (
    NotificationCategory,
    NotificationPriority,
)

from app.services.notification_dispatcher_service import (
    NotificationDispatcherService,
)

from app.services.notification_template_service import (
    NotificationTemplateService,
)


class NotificationService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _send(
        recipient,
        subject,
        message,
        priority=NotificationPriority.NORMAL,
        category=NotificationCategory.CUSTOMER,
        metadata=None,
    ):

        return (
            NotificationDispatcherService
            .send_notification(

                recipient=recipient,

                subject=subject,

                message=message,

                priority=priority,

                category=category,

                metadata=metadata,

            )
        )

    # ==========================================================
    # Customer Notifications
    # ==========================================================

    @staticmethod
    def send_welcome(
        customer,
    ):

        return (
            NotificationService._send(

                recipient=customer,

                subject="Welcome",

                message=(
                    NotificationTemplateService
                    .welcome(
                        customer,
                    )
                ),

                metadata={
                    "customer_id":
                        customer.customer_id,
                },

            )
        )

    @staticmethod
    def send_payment_success(
        payment,
    ):

        return (
            NotificationService._send(

                recipient=payment.customer,

                subject=(
                    "Payment Successful"
                ),

                message=(
                    NotificationTemplateService
                    .payment_success(
                        payment,
                    )
                ),

                metadata={

                    "payment_reference":
                        payment.payment_reference,

                    "customer_id":
                        payment.customer_id,

                },

            )
        )

    @staticmethod
    def send_payment_failed(
        payment,
    ):

        return (
            NotificationService._send(

                recipient=payment.customer,

                subject=(
                    "Payment Failed"
                ),

                message=(
                    NotificationTemplateService
                    .payment_failed(
                        payment,
                    )
                ),

                priority=(
                    NotificationPriority.HIGH
                ),

                metadata={

                    "payment_reference":
                        payment.payment_reference,

                    "customer_id":
                        payment.customer_id,

                },

            )
        )

    @staticmethod
    def send_subscription_created(
        subscription,
    ):

        return (
            NotificationService._send(

                recipient=subscription.customer,

                subject=(
                    "Subscription Activated"
                ),

                message=(
                    NotificationTemplateService
                    .subscription_created(
                        subscription,
                    )
                ),

                metadata={

                    "subscription_id":
                        subscription.subscription_id,

                    "customer_id":
                        subscription.customer_id,

                },

            )
        )

    @staticmethod
    def send_subscription_expiring(
        subscription,
        days_remaining,
    ):

        return (
            NotificationService._send(

                recipient=subscription.customer,

                subject=(
                    "Subscription Expiring"
                ),

                message=(
                    NotificationTemplateService
                    .subscription_expiring(
                        subscription,
                        days_remaining,
                    )
                ),

                priority=(
                    NotificationPriority.HIGH
                ),

                metadata={

                    "subscription_id":
                        subscription.subscription_id,

                    "customer_id":
                        subscription.customer_id,

                },

            )
        )

    @staticmethod
    def send_subscription_expired(
        subscription,
    ):

        return (
            NotificationService._send(

                recipient=subscription.customer,

                subject=(
                    "Subscription Expired"
                ),

                message=(
                    NotificationTemplateService
                    .subscription_expired(
                        subscription,
                    )
                ),

                priority=(
                    NotificationPriority.CRITICAL
                ),

                metadata={

                    "subscription_id":
                        subscription.subscription_id,

                    "customer_id":
                        subscription.customer_id,

                },

            )
        )

    @staticmethod
    def send_device_registered(
        device,
    ):

        return (
            NotificationService._send(

                recipient=device.customer,

                subject=(
                    "New Device Registered"
                ),

                message=(
                    NotificationTemplateService
                    .device_registered(
                        device,
                    )
                ),

                metadata={

                    "device_id":
                        device.device_id,

                    "customer_id":
                        device.customer_id,

                },

            )
        )

    @staticmethod
    def send_device_blocked(
        device,
    ):

        return (
            NotificationService._send(

                recipient=device.customer,

                subject=(
                    "Device Blocked"
                ),

                message=(
                    NotificationTemplateService
                    .device_blocked(
                        device,
                    )
                ),

                priority=(
                    NotificationPriority.HIGH
                ),

                metadata={

                    "device_id":
                        device.device_id,

                    "customer_id":
                        device.customer_id,

                },

            )
        )
        
    # ==========================================================
    # Admin Notifications
    # ==========================================================

    @staticmethod
    def send_router_offline(
        router,
    ):

        return (
            NotificationService._send(

                recipient=None,

                subject=(
                    "Router Offline"
                ),

                message=(
                    NotificationTemplateService
                    .router_offline(
                        router,
                    )
                ),

                priority=(
                    NotificationPriority.CRITICAL
                ),

                category=(
                    NotificationCategory.ADMIN
                ),

                metadata={

                    "router_id":
                        router.router_id,

                },

            )
        )

    @staticmethod
    def send_router_online(
        router,
    ):

        return (
            NotificationService._send(

                recipient=None,

                subject=(
                    "Router Online"
                ),

                message=(
                    NotificationTemplateService
                    .router_online(
                        router,
                    )
                ),

                category=(
                    NotificationCategory.ADMIN
                ),

                metadata={

                    "router_id":
                        router.router_id,

                },

            )
        )

    # ==========================================================
    # System Notifications
    # ==========================================================

    @staticmethod
    def send_system_notification(
        subject,
        message,
        priority=NotificationPriority.NORMAL,
    ):

        return (
            NotificationService._send(

                recipient=None,

                subject=subject,

                message=(
                    NotificationTemplateService
                    .system_message(
                        subject,
                        message,
                    )
                ),

                priority=priority,

                category=(
                    NotificationCategory.SYSTEM
                ),

            )
        )      