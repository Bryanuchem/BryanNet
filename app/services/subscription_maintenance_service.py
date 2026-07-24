from datetime import UTC
from datetime import datetime
from datetime import timedelta

from app.enums import (
    SubscriptionStatus,
)

from app.models.subscription import (
    Subscription,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    AUTOMATION_SUBSCRIPTIONS,
)

from app.services.notification_service import (
    NotificationService,
)

from app.services.plan_service import (
    PlanService,
)

from app.services.router_provisioning_service import (
    RouterProvisioningService,
)


class SubscriptionMaintenanceService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _finalize_subscription_change(
        db,
        subscription,
        notification_callback,
    ):

        db.commit()

        db.refresh(
            subscription,
        )

        RouterProvisioningService.synchronize_customer_access(

            db,

            subscription.customer_id,

        )

        notification_callback(
            subscription,
        )

    @staticmethod
    def _activate_subscription(
        db,
        subscription,
    ):

        now = datetime.now(
            UTC,
        )

        plan = (
            PlanService.get_plan(
                db,
                subscription.plan_id,
            )
        )

        subscription.status = (
            SubscriptionStatus.ACTIVE
        )

        subscription.start_date = now

        subscription.expiry_date = (
            now
            + timedelta(
                days=plan.duration_days,
            )
        )

        subscription.activated_at = now

        SubscriptionMaintenanceService \
            ._finalize_subscription_change(

                db,

                subscription,

                NotificationService
                .send_subscription_created,

            )

    @staticmethod
    def _expire_subscription(
        db,
        subscription,
    ):

        subscription.status = (
            SubscriptionStatus.EXPIRED
        )

        SubscriptionMaintenanceService \
            ._finalize_subscription_change(

                db,

                subscription,

                NotificationService
                .send_subscription_expired,

            )

    @staticmethod
    def _activate_next_queued_subscription(
        db,
        customer_id,
    ):

        queued_subscription = (

            db.query(
                Subscription,
            )

            .filter(

                Subscription.customer_id
                == customer_id,

                Subscription.status
                == SubscriptionStatus.QUEUED,

            )

            .order_by(

                Subscription.activation_sequence,

                Subscription.created_at,

            )

            .first()

        )

        if not queued_subscription:

            return False

        SubscriptionMaintenanceService \
            ._activate_subscription(

                db,

                queued_subscription,

            )

        return True
    
    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def run(
        db,
        admin=None,
        session=None,
    ):

        now = datetime.now(
            UTC,
        )

        active_subscriptions = (

            db.query(
                Subscription,
            )

            .filter(

                Subscription.status
                == SubscriptionStatus.ACTIVE,

                Subscription.expiry_date
                <= now,

            )

            .all()

        )

        activated = 0

        expired = 0

        for subscription in active_subscriptions:

            customer_id = (
                subscription.customer_id
            )

            SubscriptionMaintenanceService \
                ._expire_subscription(

                    db,

                    subscription,

                )

            expired += 1

            if (

                SubscriptionMaintenanceService
                ._activate_next_queued_subscription(

                    db,

                    customer_id,

                )

            ):

                activated += 1

        result = {

            "processed":
                len(
                    active_subscriptions,
                ),

            "subscriptions_checked":
                len(
                    active_subscriptions,
                ),

            "expired":
                expired,

            "activated":
                activated,

        }

        AuditLogService.log_system_action(

            db=db,
            
            admin=admin,

            session=session,

            action=AUTOMATION_SUBSCRIPTIONS,

            description=(

                "Subscription maintenance processed "

                f"{result['processed']} subscription(s): "

                f"{result['expired']} expired, "

                f"{result['activated']} activated."

            ),

            entity_type="System",

            target_name="Subscriptions",

            new_values=result,

        )

        db.commit()

        return result