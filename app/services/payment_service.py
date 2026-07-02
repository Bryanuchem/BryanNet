from datetime import datetime, UTC
from uuid import uuid4
from sqlalchemy import func

from fastapi import HTTPException

from app.enums import (
    PaymentProvider,
    PaymentStatus,
)

from app.models.payment import Payment

from app.services.customer_service import CustomerService
from app.services.plan_service import PlanService
from app.services.subscription_service import (
    SubscriptionService,
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

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_payment(
        db,
        customer_id,
        plan_id,
        payment_provider: PaymentProvider,
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
    def complete_payment(
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
            SubscriptionService.create_subscription(
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
    def cancel_payment(
        db,
        payment_reference,
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

        PaymentService._mark_cancelled(
            payment,
        )

        db.commit()

        db.refresh(
            payment,
        )

        return payment

    @staticmethod
    def refund_payment(
        db,
        payment_reference,
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

        PaymentService._mark_refunded(
            payment,
        )

        db.commit()

        db.refresh(
            payment,
        )

        return payment

    @staticmethod
    def expire_payment(
        db,
        payment_reference,
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

        PaymentService._mark_expired(
            payment,
        )

        db.commit()

        db.refresh(
            payment,
        )

        return payment

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
    ):

        return (
            db.query(Payment)
            .order_by(
                Payment.created_at.desc()
            )
            .all()
        )

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