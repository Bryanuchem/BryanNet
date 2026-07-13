from sqlalchemy.orm import (
    Session,
)

from fastapi import (
    HTTPException,
)

from app.schemas.portal_payment import (
    PortalPaymentCreate,
    PortalPaymentResponse,
    PortalPaymentDetailResponse,
)
from app.services.customer_service import (
    CustomerService,
)

from app.services.payment_service import (
    PaymentService,
)

from app.services.payment_dispatcher_service import (
    PaymentDispatcherService,
)

from app.services.payment_document_service import (
    PaymentDocumentService,
)

from app.services.payment_transaction_service import (
    PaymentTransactionService,
)

from app.services.plan_service import (
    PlanService,
)

from app.enums import (
    PaymentProvider,
    PaymentChannel,
)

from app.domain.payment import (
    PaymentInitializationResult,
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
        initialization: (
            PaymentInitializationResult | None
        ) = None,
    ):

        plan = (
            PlanService.get_plan(
                db,
                payment.plan_id,
            )
        )

        subscription_queued = (

            payment.subscription is not None

            and

            payment.subscription.status.value
            == "queued"

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

            checkout_url=(

                initialization.authorization_url

                if initialization

                else None

            ),

            subscription_queued=(

                subscription_queued

            ),

            payment_date=(
                payment.payment_date
            ),

            created_at=(
                payment.created_at
            ),

        )

    @staticmethod
    def _build_payment_detail_response(
        db: Session,
        payment,
    ):

        transaction = (

            PaymentTransactionService
            .get_latest_transaction(

                db,

                payment.payment_id,

            )

        )

        return (

            PortalPaymentDetailResponse(

                payment_reference=(
                    payment.payment_reference
                ),

                plan_name=(
                    payment.plan.plan_name
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

                payment_provider=(
                    payment.payment_provider.value
                ),

                payment_channel=(
                    payment.payment_channel
                ),

                gateway_reference=(

                    transaction.gateway_reference

                    if transaction

                    else None

                ),

                gateway_transaction_id=(

                    transaction.gateway_transaction_id

                    if transaction

                    else None

                ),

                authorization_code=(

                    transaction.authorization_code

                    if transaction

                    else None

                ),

                gateway_status=(

                    transaction.gateway_status

                    if transaction

                    else None

                ),

                paid_at=(

                    transaction.paid_at

                    if transaction

                    else None

                ),

            )

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
            PaymentService._find_pending_payment(
                db=db,
                customer_id=customer.customer_id,
                plan_id=request.plan_id,
            )
        )

        if (

            payment

            and

            PaymentService._pending_payment_expired(
                payment,
            )

        ):

            PaymentService._expire_payment(
                db,
                payment,
            )

            payment = None

        if payment is None:

            payment = (
                PaymentService._create_payment(
                    db=db,
                    customer_id=customer.customer_id,
                    plan_id=request.plan_id,
                    payment_provider=PaymentProvider.PAYSTACK,
                    payment_channel=PaymentChannel.WALLET,
                )
            )

        initialization = (
            PaymentDispatcherService
            .initialize_payment(
                db,
                payment,
            )
        )

        return (
            PortalPaymentService
            ._build_payment_response(
                db,
                payment,
                initialization,
            )
        )


    @staticmethod
    def verify_payment(
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

        if payment.status.value != "pending":

            return (
                PortalPaymentService
                ._build_payment_response(
                    db,
                    payment,
                )
            )

        transaction = (
            PaymentTransactionService
            .get_latest_transaction(
                db,
                payment.payment_id,
            )
        )

        if transaction is None:

            raise HTTPException(
                status_code=404,
                detail="Payment transaction not found.",
            )

        result = (
            PaymentDispatcherService
            .verify_payment(
                db,
                transaction.transaction_id,
            )
        )

        if (
            result.verified
            and payment.status.value == "pending"
        ):

            PaymentDispatcherService.complete_payment(
                db,
                transaction.transaction_id,
            )

        payment = (
            PaymentService.get_payment(
                db,
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
    def retry_payment(
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

        old_payment = (
            PortalPaymentService
            ._get_customer_payment(
                db,
                customer,
                payment_reference,
            )
        )

        if old_payment.status.value not in (
            "failed",
            "expired",
            "cancelled",
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only failed, expired or "
                    "cancelled payments "
                    "can be retried."
                ),
            )

        payment = (
            PaymentService._create_payment(
                db=db,
                customer_id=customer.customer_id,
                plan_id=old_payment.plan_id,
                payment_provider=(
                    old_payment.payment_provider
                ),
                payment_channel=(
                    old_payment.payment_channel
                ),
            )
        )

        initialization = (
            PaymentDispatcherService
            .initialize_payment(
                db,
                payment,
            )
        )

        return (
            PortalPaymentService
            ._build_payment_response(
                db,
                payment,
                initialization,
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
        
    @staticmethod
    def get_receipt(
        db,
        telegram_user_id,
        payment_reference,
    ):

        payment = (
            PortalPaymentService.get_payment(
                db,
                telegram_user_id,
                payment_reference,
            )
        )

        return (
            PaymentDocumentService.generate_receipt_pdf(
                db,
                payment.payment_reference,
            )
        )
        
    @staticmethod
    def get_payment_by_reference(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService.get_payment(
                db,
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
    def get_payment_details(
        db,
        payment_reference,
    ):

        payment = (

            PaymentService.get_payment(

                db,

                payment_reference,

            )

        )

        return (

            PortalPaymentService

            ._build_payment_detail_response(

                db,

                payment,

            )

        )