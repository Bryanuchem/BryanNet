from app.services.notification_scheduling_service import (
    NotificationSchedulingService,
)

from app.services.payment_maintenance_service import (
    PaymentMaintenanceService,
)

from app.services.router_maintenance_service import (
    RouterMaintenanceService,
)

from app.services.subscription_maintenance_service import (
    SubscriptionMaintenanceService,
)


class AutomationService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _run_job(
        job,
        db,
    ):

        return job(
            db,
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def run_payment_jobs(
        db,
    ):

        return (
            AutomationService
            ._run_job(

                PaymentMaintenanceService
                .run,

                db,

            )
        )

    @staticmethod
    def run_subscription_jobs(
        db,
    ):

        return (
            AutomationService
            ._run_job(

                SubscriptionMaintenanceService
                .run,

                db,

            )
        )

    @staticmethod
    def run_router_jobs(
        db,
    ):

        return (
            AutomationService
            ._run_job(

                RouterMaintenanceService
                .run,

                db,

            )
        )

    @staticmethod
    def run_notification_jobs(
        db,
    ):

        return (
            AutomationService
            ._run_job(

                NotificationSchedulingService
                .run,

                db,

            )
        )

    @staticmethod
    def run_all_jobs(
        db,
    ):

        return {

            "payments": (

                AutomationService
                .run_payment_jobs(
                    db,
                )

            ),

            "subscriptions": (

                AutomationService
                .run_subscription_jobs(
                    db,
                )

            ),

            "routers": (

                AutomationService
                .run_router_jobs(
                    db,
                )

            ),

            "notifications": (

                AutomationService
                .run_notification_jobs(
                    db,
                )

            ),

        }