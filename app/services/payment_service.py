from datetime import datetime, UTC
from uuid import uuid4
from sqlalchemy import func
from typing import cast
from decimal import Decimal

from fastapi import HTTPException

from app.enums import (
    PaymentProvider,
    PaymentStatus,
)

from app.models.payment import Payment
from app.models.customer import Customer
from app.models.plan import Plan

from app.schemas.payment import (
    PaymentListItem,
)

from app.services.customer_service import CustomerService
from app.services.plan_service import PlanService
from app.services.subscription_service import (
    SubscriptionService,
)
from app.services.audit_log_service import AuditLogService
from app.enums.audit_result import AuditResult

from app.constants.audit_actions import (
    CREATE_PAYMENT,
    VERIFY_PAYMENT,
    CANCEL_PAYMENT,
    REFUND_PAYMENT,
    EXPIRE_PAYMENT,
)

class PaymentService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _generate_payment_reference():

        return (
            f"BRN-{uuid4().hex[:12].upper()}"
        )

    @staticmethod
    def _find_payment(
        db,
        payment_reference,
    ):

        payment = (
            db.query(Payment)
            .filter(
                Payment.payment_reference
                == payment_reference
            )
            .first()
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        return payment

    @staticmethod
    def _create_payment(
        db,
        customer_id,
        plan_id,
        payment_provider: PaymentProvider,
        payment_channel,
        payment_method=None,
    ):

        CustomerService.get_customer(
            db,
            customer_id,
        )

        plan = (
            PlanService.get_plan(
                db,
                plan_id,
            )
        )

        payment = Payment(

            customer_id=customer_id,

            plan_id=plan_id,

            subscription_id=None,

            amount=plan.price,

            payment_provider=payment_provider,

            payment_channel=payment_channel,

            payment_method=payment_method,

            payment_reference=(
                PaymentService
                ._generate_payment_reference()
            ),

            gateway_transaction_id=None,

            status=PaymentStatus.PENDING,

            payment_date=None,

        )

        db.add(
            payment,
        )

        db.commit()

        db.refresh(
            payment,
        )

        return payment

    @staticmethod
    def _complete_payment(
        db,
        payment_reference,
        gateway_transaction_id=None,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if (
            payment.status
            != PaymentStatus.PENDING
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only pending payments "
                    "can be completed."
                ),
            )

        PaymentService._mark_successful(
            payment,
            gateway_transaction_id,
        )

        subscription = (
            SubscriptionService._create_subscription(
                db=db,
                customer_id=payment.customer_id,
                plan_id=payment.plan_id,
            )
        )

        payment.subscription_id = (
            subscription.subscription_id
        )

        db.commit()

        db.refresh(
            payment,
        )

        return payment

    @staticmethod
    def _mark_successful(
        payment,
        gateway_transaction_id=None,
    ):

        payment.status = (
            PaymentStatus.SUCCESSFUL
        )

        payment.gateway_transaction_id = (
            gateway_transaction_id
        )

        payment.payment_date = (
            datetime.now(UTC)
        )

    @staticmethod
    def _mark_failed(
        payment,
    ):

        payment.status = (
            PaymentStatus.FAILED
        )

    @staticmethod
    def _mark_cancelled(
        payment,
    ):

        payment.status = (
            PaymentStatus.CANCELLED
        )

    @staticmethod
    def _mark_refunded(
        payment,
    ):

        payment.status = (
            PaymentStatus.REFUNDED
        )

    @staticmethod
    def _mark_expired(
        payment,
    ):

        payment.status = (
            PaymentStatus.EXPIRED
        )

    @staticmethod
    def _finalize_payment_change(
        db,
        payment,
    ):

        db.commit()

        db.refresh(
            payment,
        )

        return payment

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
    def create_payment(
        db,
        customer_id,
        plan_id,
        payment_provider: PaymentProvider,
        payment_channel,
        admin_id,
        payment_method=None,
    ):

        payment = (
            PaymentService._create_payment(
                db=db,
                customer_id=customer_id,
                plan_id=plan_id,
                payment_provider=payment_provider,
                payment_channel=payment_channel,
                payment_method=payment_method,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=CREATE_PAYMENT,

            entity_type="Payment",

            entity_id=cast(
                int,
                payment.payment_id,
            ),

            target_name=str(
                payment.payment_reference,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Payment '{str(payment.payment_reference)}' "
                "was created."
            ),

            new_values={
                "customer_id": cast(
                    int,
                    payment.customer_id,
                ),
                "plan_id": cast(
                    int,
                    payment.plan_id,
                ),
                "amount": cast(
                    float,
                    payment.amount,
                ),
                "payment_provider":
                    str(
                    payment.payment_provider.value
                    ),
                "payment_channel":
                    payment.payment_channel.value,
                "payment_method":
                    payment.payment_method,
                "status":
                    payment.status.value,
            },

        )

        return payment
    
    @staticmethod
    def complete_payment(
        db,
        payment_reference,
        admin_id,
        gateway_transaction_id=None,
    ):

        payment = (
            PaymentService._complete_payment(
                db=db,
                payment_reference=payment_reference,
                gateway_transaction_id=(
                    gateway_transaction_id
                ),
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=VERIFY_PAYMENT,

            entity_type="Payment",

            entity_id=cast(
                int,
                payment.payment_id,
            ),

            target_name=str(
                payment.payment_reference,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Payment '{str(payment.payment_reference)}' "
                "was verified."
            ),

            new_values={
                "status":
                    payment.status.value,
                "gateway_transaction_id":
                    payment.gateway_transaction_id,
                "subscription_id":
                    payment.subscription_id,
                "payment_date": (
                    payment.payment_date.isoformat()
                    if payment.payment_date
                    else None
                ),
            },

        )

        return payment
    
    @staticmethod
    def cancel_payment(
        db,
        payment_reference,
        admin_id,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if (
            payment.status
            != PaymentStatus.PENDING
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only pending payments "
                    "can be cancelled."
                ),
            )

        old_status = payment.status

        PaymentService._mark_cancelled(
            payment,
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=CANCEL_PAYMENT,

            entity_type="Payment",

            entity_id=cast(
                int,
                payment.payment_id,
            ),

            target_name=payment.payment_reference,

            result=AuditResult.SUCCESS,

            description=(
                f"Payment '{payment.payment_reference}' was cancelled."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": payment.status.value,
            },

        )

        return (
            PaymentService
            ._finalize_payment_change(
                db,
                payment,
            )
        )

    @staticmethod
    def refund_payment(
        db,
        payment_reference,
        admin_id,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if (
            payment.status
            != PaymentStatus.SUCCESSFUL
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only successful payments "
                    "can be refunded."
                ),
            )

        old_status = payment.status

        PaymentService._mark_refunded(
            payment,
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=REFUND_PAYMENT,

            entity_type="Payment",

            entity_id=cast(
                int,
                payment.payment_id,
            ),

            target_name=payment.payment_reference,

            result=AuditResult.SUCCESS,

            description=(
                f"Payment '{payment.payment_reference}' was refunded."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": payment.status.value,
            },

        )

        return (
            PaymentService
            ._finalize_payment_change(
                db,
                payment,
            )
        )

    @staticmethod
    def expire_payment(
        db,
        payment_reference,
        admin_id,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if (
            payment.status
            != PaymentStatus.PENDING
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only pending payments "
                    "can be expired."
                ),
            )

        old_status = payment.status

        PaymentService._mark_expired(
            payment,
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=EXPIRE_PAYMENT,

            entity_type="Payment",

            entity_id=cast(
                int,
                payment.payment_id,
            ),

            target_name=payment.payment_reference,

            result=AuditResult.SUCCESS,

            description=(
                f"Payment '{payment.payment_reference}' expired."
            ),

            old_values={
                "status": old_status.value,
            },

            new_values={
                "status": payment.status.value,
            },

        )

        return (
            PaymentService
            ._finalize_payment_change(
                db,
                payment,
            )
        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_payment(
        db,
        payment_reference,
    ):

        return (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

    @staticmethod
    def get_customer_payments(
        db,
        customer_id,
    ):

        CustomerService.get_customer(
            db,
            customer_id,
        )

        return (
            db.query(Payment)
            .filter(
                Payment.customer_id == customer_id,
            )
            .order_by(
                Payment.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_all_payments(
        db,
        page=1,
        page_size=25,
        search=None,
        customer_id=None,
        payment_provider=None,
        payment_channel=None,
        payment_method=None,
        status=None,
        sort_by="created_at",
        sort_order="desc",
    ):

        query = (

            db.query(

                Payment,

                Customer.full_name.label(
                    "customer_name",
                ),

                Plan.plan_name.label(
                    "plan_name",
                ),

            )

            .join(
                Customer,
                Customer.customer_id == Payment.customer_id,
            )

            .join(
                Plan,
                Plan.plan_id == Payment.plan_id,
            )

        )
        
        if search:

            query = query.filter(

                Customer.full_name.ilike(
                    f"%{search}%"
                )

                |

                Plan.plan_name.ilike(
                    f"%{search}%"
                )

                |

                Payment.payment_reference.ilike(
                    f"%{search}%"
                )

            )        

        # ==========================================================
        # Filters
        # ==========================================================

        if customer_id is not None:

            query = query.filter(
                Payment.customer_id == customer_id,
            )

        if payment_provider is not None:

            query = query.filter(
                Payment.payment_provider == payment_provider,
            )

        if payment_channel is not None:

            query = query.filter(
                Payment.payment_channel == payment_channel,
            )

        if payment_method is not None:

            query = query.filter(
                Payment.payment_method == payment_method,
            )

        if status is not None:

            query = query.filter(
                Payment.status == status,
            )

        # ==========================================================
        # Sorting
        # ==========================================================

        sort_column = {
            
            "created_at":
                Payment.created_at,

            "payment_date":
                Payment.payment_date,

            "customer_name":
                Customer.full_name,

            "plan_name":
                Plan.plan_name,

            "amount":
                Payment.amount,

            "provider":
                Payment.payment_provider,

            "channel":
                Payment.payment_channel,

            "method":
                Payment.payment_method,

            "status":
                Payment.status,

        }.get(

            sort_by,

            Payment.created_at,

        )

        query = PaymentService._apply_sort(

            query,

            sort_column,

            sort_order,

        )

        # ==========================================================
        # Pagination
        # ==========================================================

        total = query.count()

        results = (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )

        # ==========================================================
        # Response
        # ==========================================================

        payments = [

            PaymentListItem(

                payment_reference=
                    payment.payment_reference,

                customer_id=
                    payment.customer_id,

                customer_name=
                    customer_name,

                plan_id=
                    payment.plan_id,

                plan_name=
                    plan_name,

                amount=
                    payment.amount,

                payment_provider=
                    payment.payment_provider,

                payment_channel=
                    payment.payment_channel,

                payment_method=
                    payment.payment_method,

                status=
                    payment.status,

                payment_date=
                    payment.payment_date,

                created_at=
                    payment.created_at,

            )

            for (

                payment,

                customer_name,

                plan_name,

            ) in results

        ]

        return {

            "items": payments,

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": (
                (total + page_size - 1) // page_size
                if total
                else 0
            ),

        }

    @staticmethod
    def get_payment_summary(
        db,
    ):

        total_payments = (
            db.query(Payment)
            .count()
        )

        pending_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.PENDING
            )
            .count()
        )

        successful_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.SUCCESSFUL
            )
            .count()
        )

        failed_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.FAILED
            )
            .count()
        )

        cancelled_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.CANCELLED
            )
            .count()
        )

        refunded_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.REFUNDED
            )
            .count()
        )

        expired_payments = (
            db.query(Payment)
            .filter(
                Payment.status
                == PaymentStatus.EXPIRED
            )
            .count()
        )

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(
                        Payment.amount,
                    ),
                    0,
                )
            )
            .filter(
                Payment.status
                == PaymentStatus.SUCCESSFUL
            )
            .scalar()
        )

        return {

            "total_payments":
                total_payments,

            "pending_payments":
                pending_payments,

            "successful_payments":
                successful_payments,

            "failed_payments":
                failed_payments,

            "cancelled_payments":
                cancelled_payments,

            "refunded_payments":
                refunded_payments,

            "expired_payments":
                expired_payments,

            "total_revenue":
                total_revenue,

        }    