import math

from datetime import (
    datetime,
    timedelta,
)

from sqlalchemy.orm import joinedload


from fastapi import HTTPException

from app.enums import SubscriptionStatus

from app.models.subscription import Subscription

from app.schemas.subscription import SubscriptionAdminResponse
from app.services.customer_service import CustomerService
from app.services.plan_service import PlanService
from app.services.router_account_service import (
    RouterAccountService,
)

from typing import cast

from app.services.audit_log_service import (
    AuditLogService,
)

from app.enums.audit_result import (
    AuditResult,
)

from app.constants.audit_actions import (
    PURCHASE_SUBSCRIPTION,
    CANCEL_SUBSCRIPTION,
    RENEW_SUBSCRIPTION,
    EXPIRE_SUBSCRIPTION,
)

class SubscriptionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _build_admin_response(
        subscription: Subscription,
    ) -> SubscriptionAdminResponse:

        now = datetime.now()

        remaining_days = max(
            0,
            math.ceil(
                (
                    subscription.expiry_date - now
                ).total_seconds()
                / 86400
            ),
        )

        return SubscriptionAdminResponse(

            subscription_id=subscription.subscription_id,

            customer_id=subscription.customer_id,

            customer_name=subscription.customer.full_name,

            plan_id=subscription.plan_id,

            plan_name=subscription.plan.plan_name,

            price=subscription.plan.price,

            start_date=subscription.start_date,

            activated_at=subscription.activated_at,

            expiry_date=subscription.expiry_date,

            activation_sequence=subscription.activation_sequence,

            status=subscription.status,

            remaining_days=remaining_days,

            created_at=subscription.created_at,

            updated_at=subscription.updated_at,

        )

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
            + timedelta(
                days=float(duration_days),
            )
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

    @staticmethod
    def _apply_sort(
        query,
        sort_column,
        sort_order,
    ):

        if sort_order.lower() == "desc":

            return query.order_by(
                sort_column.desc(),
            )

        return query.order_by(
            sort_column.asc(),
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_subscription(
        db,
        customer_id,
        plan_id,
        admin_id=None,
    ):

        customer = (
            CustomerService.get_customer(
                db,
                customer_id,
            )
        )

        plan = (
            PlanService.get_plan(
                db,
                plan_id,
            )
        )

        active_subscription = (
            SubscriptionService
            ._has_active_subscription(
                db,
                customer_id,
            )
        )

        latest_subscription = (
            SubscriptionService
            ._get_latest_subscription(
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

            start_date = (
                datetime.now()
            )

            status = (
                SubscriptionStatus.ACTIVE
            )

        (
            start_date,
            expiry_date,
        ) = (
            SubscriptionService
            ._calculate_dates(
                start_date,
                plan.duration_days,
            )
        )

        activation_sequence = (
            SubscriptionService
            ._get_next_activation_sequence(
                db,
                customer_id,
            )
        )

        subscription = (
            SubscriptionService
            ._build_subscription(
                customer_id=customer_id,
                plan_id=plan_id,
                start_date=start_date,
                expiry_date=expiry_date,
                activation_sequence=activation_sequence,
                status=status,
            )
        )

        db.add(
            subscription,
        )

        db.flush()

        if status == SubscriptionStatus.ACTIVE:

            SubscriptionService.activate_subscription(
                db=db,
                subscription=subscription,
                commit=False,
            )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=(
                cast(int, admin_id)
            ),

            action=PURCHASE_SUBSCRIPTION,

            entity_type="Subscription",

            entity_id=cast(
                int,
                subscription.subscription_id,
            ),

            target_name=str(
                customer.full_name,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Created {status.value.lower()} subscription "
                f"for '{customer.full_name}' "
                f"using plan '{plan.plan_name}'."
            ),

            new_values={
                "plan": str(plan.plan_name),
                "status": status.value,
                "activation_sequence": int(
                    activation_sequence,
                ),
                "start_date": (
                    start_date.isoformat()
                ),
                "expiry_date": (
                    expiry_date.isoformat()
                ),
            },

        )

        db.commit()

        db.refresh(
            subscription,
        )

        RouterAccountService.synchronize_customer_access(
            db,
            customer_id,
        )

        return subscription

    @staticmethod
    def expire_subscription(
        db,
        subscription,
        commit=True,
    ):

        old_status = subscription.status

        subscription.status = (
            SubscriptionStatus.EXPIRED
        )

        AuditLogService.log_system_action(

            db=db,

            action=EXPIRE_SUBSCRIPTION,

            entity_type="Subscription",

            entity_id=cast(
                int,
                subscription.subscription_id,
            ),

            target_name=str(
                subscription.customer.full_name,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Expired subscription for "
                f"'{subscription.customer.full_name}'."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": subscription.status.value,
            },

        )

        if commit:

            db.commit()

            db.refresh(
                subscription,
            )

            RouterAccountService.synchronize_customer_access(
                db,
                subscription.customer_id,
            )

        return subscription

    @staticmethod
    def activate_subscription(
        db,
        subscription,
        commit=True,
    ):

        old_status = subscription.status

        subscription.status = (
            SubscriptionStatus.ACTIVE
        )

        subscription.activated_at = (
            datetime.now()
        )

        AuditLogService.log_system_action(

            db=db,

            action=RENEW_SUBSCRIPTION,

            entity_type="Subscription",

            entity_id=cast(
                int,
                subscription.subscription_id,
            ),

            target_name=str(
                subscription.customer.full_name,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Activated subscription for "
                f"'{subscription.customer.full_name}'."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": subscription.status.value,
                "activated_at": (
                    subscription.activated_at.isoformat()
                ),
            },

        )

        if commit:

            db.commit()

            db.refresh(
                subscription,
            )

            RouterAccountService.synchronize_customer_access(
                db,
                subscription.customer_id,
            )

        return subscription

    @staticmethod
    def cancel_queued_subscription(
        db,
        subscription_id,
        admin_id,
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

        old_status = subscription.status

        subscription.status = (
            SubscriptionStatus.CANCELLED
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=CANCEL_SUBSCRIPTION,

            entity_type="Subscription",

            entity_id=cast(
                int,
                subscription.subscription_id,
            ),

            target_name=str(
                subscription.customer.full_name,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Cancelled queued subscription "
                f"for '{subscription.customer.full_name}'."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": subscription.status.value,
            },

        )

        db.commit()

        db.refresh(
            subscription,
        )

        return subscription

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_subscription(
        db,
        subscription_id,
    ):

        subscription = (
            db.query(
                Subscription,
            )
            .options(
                joinedload(
                    Subscription.customer,
                ),
                joinedload(
                    Subscription.plan,
                ),
            )
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

        return SubscriptionService._build_admin_response(
            subscription,
        )

    @staticmethod
    def get_active_subscription(
        db,
        customer_id,
    ):

        return (
            db.query(Subscription)
            .filter(
                Subscription.customer_id
                == customer_id,
                Subscription.status
                == SubscriptionStatus.ACTIVE,
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
                Subscription.customer_id
                == customer_id,
                Subscription.status
                == SubscriptionStatus.QUEUED,
            )
            .order_by(
                Subscription.activation_sequence
            )
            .all()
        )

    @staticmethod
    def get_customer_subscriptions(
        db,
        customer_id,
    ):

        subscriptions = (

            db.query(
                Subscription,
            )

            .options(

                joinedload(
                    Subscription.customer,
                ),

                joinedload(
                    Subscription.plan,
                ),

            )

            .filter(
                Subscription.customer_id
                == customer_id
            )

            .order_by(
                Subscription.activation_sequence
            )

            .all()

        )

        return [

            SubscriptionService._build_admin_response(
                subscription,
            )

            for subscription in subscriptions

        ]
    
    @staticmethod
    def get_customer_subscription_status(
        db,
        customer_id,
    ):

        active_subscription = (
            SubscriptionService
            .get_active_subscription(
                db,
                customer_id,
            )
        )

        queued_subscriptions = (
            SubscriptionService
            .get_queued_subscriptions(
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
            PlanService.get_plan(
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
        page=1,
        page_size=25,
        customer_id=None,
        plan_id=None,
        status=None,
        sort_by="created_at",
        sort_order="desc",
    ):

        query = (

            db.query(
                Subscription,
            )

            .options(

                joinedload(
                    Subscription.customer,
                ),

                joinedload(
                    Subscription.plan,
                ),

            )

        )

        if customer_id is not None:

            query = query.filter(
                Subscription.customer_id == customer_id,
            )

        if plan_id is not None:

            query = query.filter(
                Subscription.plan_id == plan_id,
            )

        if status is not None:

            query = query.filter(
                Subscription.status == status,
            )

        sort_column = {

            "created_at":
                Subscription.created_at,

            "expiry_date":
                Subscription.expiry_date,

            "activation_sequence":
                Subscription.activation_sequence,

        }.get(

            sort_by,

            Subscription.created_at,

        )

        query = (
            SubscriptionService._apply_sort(
                query,
                sort_column,
                sort_order,
            )
        )

        subscriptions = (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )

        return [

            SubscriptionService._build_admin_response(
                subscription,
            )

            for subscription in subscriptions

        ]