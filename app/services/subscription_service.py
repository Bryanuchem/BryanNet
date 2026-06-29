from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException

from app.models.customer import Customer
from app.models.plan import Plan
from app.models.subscription import Subscription

from app.services.subscription_history_service import (
    SubscriptionHistoryService
)

from app.services.payment_service import (
    PaymentService
)


class SubscriptionService:

    @staticmethod
    def buy_plan(
        db,
        customer_id,
        plan_id
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
                detail="Plan not found"
            )

        latest_subscription = (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id
            )
            .order_by(
                Subscription.expiry_date.desc()
            )
            .first()
        )

        now = datetime.now()

        if latest_subscription:

            start_date = (
                latest_subscription.expiry_date
            )

            status = "queued"

            sequence = (
                latest_subscription.activation_sequence
                + 1
            )

        else:

            start_date = now

            status = "active"

            sequence = 1

        expiry_date = (
            start_date
            + timedelta(
                days=plan.duration_days
            )
        )

        subscription = Subscription(
            customer_id=customer_id,
            plan_id=plan_id,
            start_date=start_date,
            expiry_date=expiry_date,
            activation_sequence=sequence,
            status=status
        )

        db.add(subscription)

        db.flush()

        PaymentService.create_payment(
            db=db,
            customer_id=customer_id,
            subscription_id=subscription.subscription_id,
            amount=plan.price,
            payment_method="wallet"
        )

        SubscriptionHistoryService.log_status_change(
            db=db,
            subscription_id=subscription.subscription_id,
            old_status=None,
            new_status=status,
            reason="Subscription purchased"
        )

        db.commit()

        db.refresh(subscription)

        return subscription

    @staticmethod
    def get_all_subscriptions(db):

        subscriptions = (
            db.query(
                Subscription,
                Customer,
                Plan
            )
            .join(
                Customer,
                Subscription.customer_id == Customer.customer_id
            )
            .join(
                Plan,
                Subscription.plan_id == Plan.plan_id
            )
            .order_by(
                Subscription.created_at.desc()
            )
            .all()
        )

        results = []

        for subscription, customer, plan in subscriptions:

            customer_name = customer.full_name

            results.append(
                {
                    "subscription_id": subscription.subscription_id,
                    "customer_id": customer.customer_id,
                    "customer_name": customer_name,
                    "plan_id": plan.plan_id,
                    "plan_name": plan.plan_name,
                    "price": float(plan.price),
                    "start_date": subscription.start_date,
                    "expiry_date": subscription.expiry_date,
                    "remaining_days": max(
                        0,
                        (subscription.expiry_date - datetime.now()).days
                    ),
                    "activation_sequence": (
                        subscription.activation_sequence
                    ),
                    "status": subscription.status,
                    "created_at": subscription.created_at,
                    "updated_at": subscription.updated_at,
                }
            )

        return results

    @staticmethod
    def get_subscription(
        db,
        subscription_id
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
                detail="Subscription not found"
            )

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id
                == subscription.customer_id
            )
            .first()
        )

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id
                == subscription.plan_id
            )
            .first()
        )

        customer_name = customer.full_name

        return {
            "subscription_id": subscription.subscription_id,
            "customer_id": customer.customer_id,
            "customer_name": customer_name,
            "plan_id": plan.plan_id,
            "plan_name": plan.plan_name,
            "price": float(plan.price),
            "start_date": subscription.start_date,
            "expiry_date": subscription.expiry_date,
            "remaining_days": max(
                0,
                (subscription.expiry_date - datetime.now()).days
            ),
            "activation_sequence": (
                subscription.activation_sequence
            ),
            "status": subscription.status,
            "created_at": subscription.created_at,
            "updated_at": subscription.updated_at,
        }

    @staticmethod
    def update_subscription(
        db,
        subscription_id,
        subscription_data
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.subscription_id == subscription_id
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        update_data = subscription_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                subscription,
                field,
                value
            )

        db.commit()

        db.refresh(subscription)

        return subscription

    @staticmethod
    def update_subscription_status(
        db,
        subscription_id,
        status
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.subscription_id == subscription_id
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        old_status = subscription.status

        subscription.status = status

        SubscriptionHistoryService.log_status_change(
            db=db,
            subscription_id=subscription.subscription_id,
            old_status=old_status,
            new_status=status,
            reason="Status updated by administrator"
        )

        db.commit()

        db.refresh(subscription)

        return subscription

    @staticmethod
    def renew_subscription(
        db,
        subscription_id
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.subscription_id == subscription_id
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        return SubscriptionService.buy_plan(
            db=db,
            customer_id=subscription.customer_id,
            plan_id=subscription.plan_id
        )

    @staticmethod
    def delete_subscription(
        db,
        subscription_id
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.subscription_id == subscription_id
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        db.delete(subscription)

        db.commit()

        return {
            "message": "Subscription deleted successfully"
        }

    @staticmethod
    def get_status(
        db,
        customer_id
    ):

        active_subscription = (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == "active"
            )
            .first()
        )

        queued_count = (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == "queued"
            )
            .count()
        )

        if not active_subscription:

            return {
                "plan_name": None,
                "status": None,
                "expiry_date": None,
                "queued_subscriptions": queued_count
            }

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id ==
                active_subscription.plan_id
            )
            .first()
        )

        return {
            "plan_name": plan.plan_name,
            "status": active_subscription.status,
            "expiry_date": active_subscription.expiry_date.isoformat(),
            "queued_subscriptions": queued_count
        }

    @staticmethod
    def get_active_subscription(
        db,
        customer_id
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id == customer_id,
                Subscription.status == "active"
            )
            .first()
        )

    @staticmethod
    def process_subscriptions(db):

        expired_subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.expiry_date < datetime.now()
            )
            .all()
        )

        processed_count = 0

        for subscription in expired_subscriptions:

            subscription.status = "expired"

            SubscriptionHistoryService.log_status_change(
                db=db,
                subscription_id=subscription.subscription_id,
                old_status="active",
                new_status="expired",
                reason="Subscription expired"
            )

            next_subscription = (
                db.query(Subscription)
                .filter(
                    Subscription.customer_id
                    == subscription.customer_id,
                    Subscription.status == "queued"
                )
                .order_by(
                    Subscription.activation_sequence
                )
                .first()
            )

            if next_subscription:

                next_subscription.status = "active"

                SubscriptionHistoryService.log_status_change(
                    db=db,
                    subscription_id=next_subscription.subscription_id,
                    old_status="queued",
                    new_status="active",
                    reason="Previous subscription expired"
                )

            processed_count += 1

        db.commit()

        return {
            "processed_subscriptions": processed_count
        }