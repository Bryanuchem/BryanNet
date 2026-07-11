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
        admin=None,
        session=None,
    ):

        return (
            PaymentMaintenanceService
            .run(
                db,
                admin=admin,
                session=session,
            )
        )

    @staticmethod
    def run_subscription_jobs(
        db,
        admin=None,
        session=None,
    ):

        return (
            SubscriptionMaintenanceService
            .run(
                db,
                admin=admin,
                session=session,
            )
        )

    @staticmethod
    def run_router_jobs(
        db,
        admin=None,
        session=None,
    ):

        return (
            RouterMaintenanceService
            .run(
                db,
                admin=admin,
                session=session,
            )
        )

    @staticmethod
    def run_notification_jobs(
        db,
        admin=None,
        session=None,
    ):

        return (
            NotificationSchedulingService
            .run(
                db,
                admin=admin,
                session=session,
            )
        )

    @staticmethod
    def run_all_jobs(
        db,
        admin=None,
        session=None,
    ):

        return {

            "payments": (

                AutomationService
                .run_payment_jobs(
                    db,
                    admin=admin,
                    session=session,
                )

            ),

            "subscriptions": (

                AutomationService
                .run_subscription_jobs(
                    db,
                    admin=admin,
                    session=session,
                )

            ),

            "routers": (

                AutomationService
                .run_router_jobs(
                    db,
                    admin=admin,
                    session=session,
                )

            ),

            "notifications": (

                AutomationService
                .run_notification_jobs(
                    db,
                    admin=admin,
                    session=session,
                )

            ),

        }