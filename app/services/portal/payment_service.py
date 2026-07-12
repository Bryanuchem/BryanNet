from sqlalchemy.orm import (
    Session,
)

from fastapi import (
    HTTPException,
)

from app.schemas.portal_payment import (
    PortalPaymentCreate,
    PortalPaymentResponse,
)

from app.services.customer_service import (
    CustomerService,
)

from app.services.payment_service import (
    PaymentService,
)

from app.services.plan_service import (
    PlanService,
)

from app.enums import (
    PaymentProvider,
    PaymentChannel,
)

class PortalPaymentService:

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
    def _get_customer_payment(
        db: Session,
        customer,
        payment_reference: str,
    ):

        payment = (
            PaymentService._find_payment(
                db,
                payment_reference,
            )
        )

        if (
            payment.customer_id
            != customer.customer_id
        ):

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        return payment

    @staticmethod
    def _build_payment_response(
        db: Session,
        payment,
    ):

        plan = (
            PlanService.get_plan(
                db,
                payment.plan_id,
            )
        )

        return PortalPaymentResponse(

            payment_reference=(
                payment.payment_reference
            ),

            plan_name=(
                plan.plan_name
            ),

            amount=(
                payment.amount
            ),

            status=(
                payment.status
            ),

            checkout_url=None,

            payment_date=(
                payment.payment_date
            ),

            created_at=(
                payment.created_at
            ),

        )

    # ==========================================================
    # Public Methods
    # ==========================================================
    
    @staticmethod
    def initialize_payment(
        db: Session,
        request: PortalPaymentCreate,
    ):

        customer = (
            PortalPaymentService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        payment = (
            PaymentService._create_payment(
                db=db,
                customer_id=customer.customer_id,
                plan_id=request.plan_id,
                payment_provider=PaymentProvider.PAYSTACK,
                payment_channel=PaymentChannel.WALLET,
            )
        )

        return (
            PortalPaymentService
            ._build_payment_response(
                db,
                payment,
            )
        )

    @staticmethod
    def get_payment(
        db: Session,
        telegram_user_id: int,
        payment_reference: str,
    ):

        customer = (
            PortalPaymentService._get_customer(
                db,
                telegram_user_id,
            )
        )

        payment = (
            PortalPaymentService
            ._get_customer_payment(
                db,
                customer,
                payment_reference,
            )
        )

        return (
            PortalPaymentService
            ._build_payment_response(
                db,
                payment,
            )
        )

    @staticmethod
    def get_customer_payments(
        db: Session,
        telegram_user_id: int,
    ):

        customer = (
            PortalPaymentService._get_customer(
                db,
                telegram_user_id,
            )
        )

        payments = (
            PaymentService.get_customer_payments(
                db,
                customer.customer_id,
            )
        )

        return [

            PortalPaymentService
            ._build_payment_response(
                db,
                payment,
            )

            for payment in payments

        ]