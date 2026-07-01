from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException

from sqlalchemy import func

from app.enums import PaymentStatus

from app.models.customer import Customer
from app.models.payment import Payment
from app.models.plan import Plan

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

        return (
            db.query(Payment)
            .filter(
                Payment.payment_reference
                == payment_reference
            )
            .first()
        )

    @staticmethod
    def _mark_successful(
        payment,
    ):

        payment.status = (
            PaymentStatus.SUCCESSFUL
        )

        payment.payment_date = (
            datetime.utcnow()
        )

    @staticmethod
    def _mark_failed(
        payment,
    ):

        payment.status = (
            PaymentStatus.FAILED
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_payment(
        db,
        customer_id,
        plan_id,
        payment_channel,
        payment_method=None,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id
                == customer_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id
                == plan_id
            )
            .first()
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found.",
            )

        payment = Payment(

            customer_id=customer_id,

            subscription_id=None,

            amount=plan.price,

            payment_channel=payment_channel,

            payment_method=payment_method,

            payment_reference=(
                PaymentService
                ._generate_payment_reference()
            ),

            status=PaymentStatus.PENDING,

            payment_date=None,

        )

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def verify_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService
            ._find_payment(
                db,
                payment_reference,
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        #
        # Payment Provider Verification
        #
        # Flutterwave
        # Paystack
        # etc.
        #

        gateway_success = True

        if not gateway_success:

            PaymentService._mark_failed(
                payment
            )

            db.commit()

            db.refresh(payment)

            return payment

        PaymentService._mark_successful(
            payment
        )

        subscription = (
            SubscriptionService
            .create_subscription(
                db=db,
                customer_id=payment.customer_id,
                plan_id=payment.plan_id,
            )
        )

        payment.subscription_id = (
            subscription.subscription_id
        )

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def cancel_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService
            ._find_payment(
                db,
                payment_reference,
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        if payment.status != (
            PaymentStatus.PENDING
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only pending payments "
                    "can be cancelled."
                ),
            )

        payment.status = (
            PaymentStatus.CANCELLED
        )

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def refund_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService
            ._find_payment(
                db,
                payment_reference,
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        if payment.status != (
            PaymentStatus.SUCCESSFUL
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only successful payments "
                    "can be refunded."
                ),
            )

        payment.status = (
            PaymentStatus.REFUNDED
        )

        db.commit()

        db.refresh(payment)

        return payment

    # ==========================================================
    # Payment Gateway
    # ==========================================================

    @staticmethod
    def process_webhook(
        db,
        payload,
    ):
        """
        Placeholder for payment gateway webhooks.

        Flutterwave
        Paystack
        etc.
        """

        payment_reference = payload.get(
            "payment_reference"
        )

        return PaymentService.verify_payment(
            db=db,
            payment_reference=payment_reference,
        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        return payment

    @staticmethod
    def get_customer_payments(
        db,
        customer_id,
    ):

        return (
            db.query(Payment)
            .filter(
                Payment.customer_id == customer_id
            )
            .order_by(
                Payment.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_all_payments(db):

        return (
            db.query(Payment)
            .order_by(
                Payment.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_payment_summary(db):

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

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(
                        Payment.amount
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

            "total_revenue":
                total_revenue,

        }   