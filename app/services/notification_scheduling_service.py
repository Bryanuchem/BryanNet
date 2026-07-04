from datetime import UTC
from datetime import datetime

from app.enums import SubscriptionStatus

from app.models.subscription import (
    Subscription,
)

from app.services.notification_service import (
    NotificationService,
)


class NotificationSchedulingService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _days_remaining(
        subscription,
    ):

        now = datetime.now(
            UTC,
        ).date()

        end_date = (
            subscription.expiry_date.date()
        )

        return (
            end_date - now
        ).days

    # ==========================================================
    # Business Commands
    # ==========================================================

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def run(
        db,
    ):

        subscriptions = (

            db.query(
                Subscription,
            )

            .filter(

                Subscription.status
                == SubscriptionStatus.ACTIVE,

            )

            .all()

        )

        reminders_sent = 0

        expired_sent = 0

        for subscription in subscriptions:

            days_remaining = (

                NotificationSchedulingService
                ._days_remaining(
                    subscription,
                )

            )

            if days_remaining in (
                7,
                3,
                1,
            ):

                NotificationService.send_subscription_expiring(

                    subscription,

                    days_remaining,

                )

                reminders_sent += 1

            elif days_remaining <= 0:

                NotificationService.send_subscription_expired(

                    subscription,

                )

                expired_sent += 1

        return {

            "processed":
                len(subscriptions),

            "subscriptions_checked":
                len(subscriptions),

            "expiry_reminders_sent":
                reminders_sent,

            "expired_notifications_sent":
                expired_sent,

        }

    @staticmethod
    def send_daily_admin_summary(
        db,
    ):
        """
        Placeholder.

        Future implementation:

        • New customers

        • New subscriptions

        • Payments received

        • Routers offline

        • Active customers

        """

        return {

            "success": True,

            "message":
                "Daily admin summary placeholder.",

        }

    @staticmethod
    def process_notification_queue():
        """
        Placeholder.

        Future implementation:

        • Retry failed notifications

        • Process queued notifications

        • Rate limiting

        • Background workers

        """

        return {

            "success": True,

            "message":
                "Notification queue placeholder.",

        }