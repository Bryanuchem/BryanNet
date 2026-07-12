from datetime import (
    datetime,
)

from fastapi import (
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.schemas.portal_subscription import (
    PortalSubscriptionPurchase,
    PortalSubscriptionActionRequest,
    PortalSubscriptionResponse,
)

from app.services.customer_service import (
    CustomerService,
)

from app.services.plan_service import (
    PlanService,
)

from app.services.subscription_service import (
    SubscriptionService,
)


class PortalSubscriptionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_customer(
        db: Session,
        telegram_user_id: int,
    ):

        customer = (
            CustomerService.get_customer_by_telegram_id(
                db,
                telegram_user_id,
            )
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        return customer

    @staticmethod
    def _get_customer_subscription(
        db: Session,
        customer,
        subscription_id: int,
    ):

        subscription = (
            SubscriptionService._find_subscription(
                db,
                subscription_id,
            )
        )

        if (
            subscription.customer_id
            != customer.customer_id
        ):

            raise HTTPException(
                status_code=404,
                detail="Subscription not found.",
            )

        return subscription

    @staticmethod
    def _build_subscription_response(
        db: Session,
        customer,
    ):

        subscription = (
            SubscriptionService.get_active_subscription(
                db,
                customer.customer_id,
            )
        )

        queued_subscriptions = (
            SubscriptionService.get_queued_subscriptions(
                db,
                customer.customer_id,
            )
        )

        if not subscription:

            raise HTTPException(
                status_code=404,
                detail=(
                    "No active subscription found."
                ),
            )

        plan = (
            PlanService.get_plan(
                db,
                subscription.plan_id,
            )
        )

        remaining_days = max(
            0,
            (
                subscription.expiry_date
                - datetime.now()
            ).days,
        )

        return PortalSubscriptionResponse(

            subscription_id=(
                subscription.subscription_id
            ),

            has_active_subscription=
            subscription is not None,

            plan_name=(
                plan.plan_name
            ),

            price=float(
                plan.price
            ),

            speed_limit_mbps=(
                plan.speed_limit_mbps
            ),

            max_devices=(
                plan.max_devices
            ),

            concurrent_devices=(
                plan.concurrent_devices
            ),

            start_date=(
                subscription.start_date
            ),

            expiry_date=(
                subscription.expiry_date
            ),

            activated_at=(
                subscription.activated_at
            ),

            activation_sequence=(
                subscription.activation_sequence
            ),

            status=(
                subscription.status
            ),

            queued_subscriptions=len(
                queued_subscriptions
            ),

            remaining_days=(
                remaining_days
            ),

        )

    # ==========================================================
    # Public Methods
    # ==========================================================
    
    @staticmethod
    def get_subscription_status(
        db: Session,
        telegram_user_id: int,
    ):

        customer = (
            PortalSubscriptionService._get_customer(
                db,
                telegram_user_id,
            )
        )

        return (
            PortalSubscriptionService
            ._build_subscription_response(
                db,
                customer,
            )
        )

    @staticmethod
    def purchase_subscription(
        db: Session,
        request: PortalSubscriptionPurchase,
    ):

        customer = (
            PortalSubscriptionService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        SubscriptionService._create_subscription(
            db,
            customer.customer_id,
            request.plan_id,
        )

        return (
            PortalSubscriptionService
            ._build_subscription_response(
                db,
                customer,
            )
        )

    @staticmethod
    def cancel_subscription(
        db: Session,
        subscription_id: int,
        request: PortalSubscriptionActionRequest,
    ):

        customer = (
            PortalSubscriptionService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        PortalSubscriptionService._get_customer_subscription(
            db,
            customer,
            subscription_id,
        )

        SubscriptionService._cancel_queued_subscription(
            db,
            subscription_id,
        )

        return (
            PortalSubscriptionService
            ._build_subscription_response(
                db,
                customer,
            )
        )    