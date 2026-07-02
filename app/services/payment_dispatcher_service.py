from fastapi import HTTPException

from app.providers.payment.factory import (
    PaymentProviderFactory,
)

from app.services.payment_service import (
    PaymentService,
)


class PaymentDispatcherService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_provider(
        payment,
    ):

        return (
            PaymentProviderFactory.get_provider(
                payment.payment_provider,
            )
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def initialize_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService.get_payment(
                db,
                payment_reference,
            )
        )

        provider = (
            PaymentDispatcherService
            ._get_provider(
                payment,
            )
        )

        return (
            provider.initialize_payment(
                payment,
            )
        )

    @staticmethod
    def verify_payment(
        db,
        payment_reference,
    ):

        payment = (
            PaymentService.get_payment(
                db,
                payment_reference,
            )
        )

        provider = (
            PaymentDispatcherService
            ._get_provider(
                payment,
            )
        )

        verification = (
            provider.verify_payment(
                payment_reference,
            )
        )

        if not verification.get(
            "verified",
            False,
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Payment verification failed."
                ),
            )

        return (
            PaymentService.complete_payment(
                db=db,
                payment_reference=payment_reference,
                gateway_transaction_id=(
                    verification.get(
                        "gateway_transaction_id",
                    )
                ),
            )
        )