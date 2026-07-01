from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException

from app.enums import SubscriptionStatus

from app.models.customer import Customer
from app.models.plan import Plan
from app.models.subscription import Subscription


class SubscriptionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_customer(
        db,
        customer_id,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        return customer

    @staticmethod
    def _find_plan(
        db,
        plan_id,
    ):

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id == plan_id
            )
            .first()
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        return plan

    @staticmethod
    def _find_subscription(
        db,
        subscription_id,
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.subscription_id
                == subscription_id
            )
            .first()
        )

        if not subscription:

            raise HTTPException(
                status_code=404,
                detail="Subscription not found.",
            )

        return subscription

    @staticmethod
    def _has_active_subscription(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == SubscriptionStatus.ACTIVE,
            )
            .first()
        )

    @staticmethod
    def _get_latest_subscription(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id
            )
            .order_by(
                Subscription.activation_sequence.desc()
            )
            .first()
        )

    @staticmethod
    def _get_next_activation_sequence(
        db,
        customer_id,
    ):

        latest_subscription = (
            SubscriptionService._get_latest_subscription(
                db,
                customer_id,
            )
        )

        if not latest_subscription:

            return 1

        return (
            latest_subscription.activation_sequence
            + 1
        )

    @staticmethod
    def _calculate_dates(
        start_date,
        duration_days,
    ):

        expiry_date = (
            start_date
            + timedelta(days=duration_days)
        )

        return (
            start_date,
            expiry_date,
        )

    @staticmethod
    def _build_subscription(
        customer_id,
        plan_id,
        start_date,
        expiry_date,
        activation_sequence,
        status,
    ):

        return Subscription(

            customer_id=customer_id,

            plan_id=plan_id,

            start_date=start_date,

            expiry_date=expiry_date,

            activation_sequence=activation_sequence,

            status=status,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_subscription(
        db,
        customer_id,
        plan_id,
    ):

        SubscriptionService._find_customer(
            db,
            customer_id,
        )

        plan = (
            SubscriptionService._find_plan(
                db,
                plan_id,
            )
        )

        active_subscription = (
            SubscriptionService._has_active_subscription(
                db,
                customer_id,
            )
        )

        latest_subscription = (
            SubscriptionService._get_latest_subscription(
                db,
                customer_id,
            )
        )

        if active_subscription:

            start_date = (
                latest_subscription.expiry_date
            )

            status = (
                SubscriptionStatus.QUEUED
            )

        else:

            start_date = datetime.now()

            status = (
                SubscriptionStatus.ACTIVE
            )

        (
            start_date,
            expiry_date,
        ) = (
            SubscriptionService._calculate_dates(
                start_date,
                plan.duration_days,
            )
        )

        activation_sequence = (
            SubscriptionService._get_next_activation_sequence(
                db,
                customer_id,
            )
        )

        subscription = (
            SubscriptionService._build_subscription(
                customer_id=customer_id,
                plan_id=plan_id,
                start_date=start_date,
                expiry_date=expiry_date,
                activation_sequence=activation_sequence,
                status=status,
            )
        )

        db.add(subscription)

        db.flush()

        if status == SubscriptionStatus.ACTIVE:

            SubscriptionService.activate_subscription(
                db=db,
                subscription=subscription,
                commit=False,
            )

        db.commit()

        db.refresh(subscription)

        return subscription
    
    @staticmethod
    def activate_subscription(
        db,
        subscription,
        commit=True,
    ):

        subscription.status = SubscriptionStatus.ACTIVE
        subscription.activated_at = datetime.now()

        if commit:

            db.commit()

            db.refresh(subscription)

        return subscription

    @staticmethod
    def expire_subscription(
        db,
        subscription,
        commit=True,
    ):

        subscription.status = SubscriptionStatus.EXPIRED

        if commit:

            db.commit()

            db.refresh(subscription)

        return subscription

    @staticmethod
    def activate_next_subscription(
        db,
        customer_id,
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == SubscriptionStatus.QUEUED,
            )
            .order_by(
                Subscription.activation_sequence
            )
            .first()
        )

        if not subscription:

            return None

        return (
            SubscriptionService.activate_subscription(
                db=db,
                subscription=subscription,
            )
        )

    @staticmethod
    def cancel_queued_subscription(
        db,
        subscription_id,
    ):

        subscription = (
            SubscriptionService._find_subscription(
                db,
                subscription_id,
            )
        )

        if (
            subscription.status
            != SubscriptionStatus.QUEUED
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only queued subscriptions "
                    "can be cancelled."
                ),
            )

        subscription.status = (
            SubscriptionStatus.CANCELLED
        )

        db.commit()

        db.refresh(subscription)

        return subscription

    # ==========================================================
    # Background Tasks
    # ==========================================================

    @staticmethod
    def process_expired_subscriptions(
        db,
    ):

        expired_subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status
                == SubscriptionStatus.ACTIVE,
                Subscription.expiry_date
                <= datetime.now(),
            )
            .all()
        )

        processed_count = 0

        for subscription in expired_subscriptions:

            SubscriptionService.expire_subscription(
                db=db,
                subscription=subscription,
                commit=False,
            )

            SubscriptionService.activate_next_subscription(
                db=db,
                customer_id=subscription.customer_id,
            )

            processed_count += 1

        db.commit()

        return {
            "processed_subscriptions":
                processed_count,
        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_subscription(
        db,
        subscription_id,
    ):

        return (
            SubscriptionService._find_subscription(
                db,
                subscription_id,
            )
        )

    @staticmethod
    def get_active_subscription(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == SubscriptionStatus.ACTIVE,
            )
            .first()
        )

    @staticmethod
    def get_queued_subscriptions(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == SubscriptionStatus.QUEUED,
            )
            .order_by(
                Subscription.activation_sequence,
            )
            .all()
        )

    @staticmethod
    def get_customer_subscriptions(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
            )
            .order_by(
                Subscription.activation_sequence,
            )
            .all()
        )

    @staticmethod
    def get_customer_subscription_status(
        db,
        customer_id,
    ):

        active_subscription = (
            SubscriptionService.get_active_subscription(
                db,
                customer_id,
            )
        )

        queued_subscriptions = (
            SubscriptionService.get_queued_subscriptions(
                db,
                customer_id,
            )
        )

        if not active_subscription:

            return {
                "has_active_subscription": False,
                "active_subscription": None,
                "queued_subscriptions": len(
                    queued_subscriptions
                ),
            }

        plan = (
            SubscriptionService._find_plan(
                db,
                active_subscription.plan_id,
            )
        )

        return {
            "has_active_subscription": True,
            "plan_name": plan.plan_name,
            "expiry_date": active_subscription.expiry_date,
            "queued_subscriptions": len(
                queued_subscriptions
            ),
        }

    @staticmethod
    def get_all_subscriptions(
        db,
    ):

        return (
            db.query(Subscription)
            .order_by(
                Subscription.created_at.desc(),
            )
            .all()
        )    