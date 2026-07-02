from app.providers.notification.factory import (
    NotificationProviderFactory,
)

from app.schemas.notification import (
    NotificationRequest,
)


class NotificationDispatcherService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_provider():

        #
        # Future:
        #
        # Read from application settings.
        #
        # Telegram
        # Email
        # SMS
        #

        return (
            NotificationProviderFactory
            .get_provider(
                "telegram",
            )
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def send_notification(
        recipient,
        subject,
        message,
        priority,
        category,
        metadata=None,
    ):

        notification = (
            NotificationRequest(

                recipient=recipient,

                subject=subject,

                message=message,

                priority=priority,

                category=category,

                metadata=metadata,

            )
        )

        provider = (
            NotificationDispatcherService
            ._get_provider()
        )

        return (
            provider.send(
                notification,
            )
        )