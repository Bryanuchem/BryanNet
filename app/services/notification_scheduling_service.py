from datetime import UTC
from datetime import datetime

from app.enums import SubscriptionStatus

from app.models.subscription import (
    Subscription,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    AUTOMATION_REMINDERS,
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
        admin=None,
        session=None,
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

        result = {

            "processed":
                len(subscriptions),

            "subscriptions_checked":
                len(subscriptions),

            "expiry_reminders_sent":
                reminders_sent,

            "expired_notifications_sent":
                expired_sent,

        }

        AuditLogService.log_system_action(

            db=db,
            
            admin=admin,

            session=session,

            action=AUTOMATION_REMINDERS,

            description=(

                "Notification scheduler checked "

                f"{result['subscriptions_checked']} subscription(s): "

                f"{result['expiry_reminders_sent']} reminder(s) sent, "

                f"{result['expired_notifications_sent']} expiration notification(s) sent."

            ),

            entity_type="System",

            target_name="Notifications",

            new_values=result,

        )

        db.commit()

        return result

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