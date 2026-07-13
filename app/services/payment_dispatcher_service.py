from app.domain.payment import (
    PaymentInitializationResult,
    PaymentValidationResult,
    PaymentVerificationResult,
    PaymentWebhookResult,
)

from app.services.payment_service import (
    PaymentService,
)

from app.services.payment_transaction_service import (
    PaymentTransactionService,
)

from app.providers.payment.factory import (
    PaymentProviderFactory,
)


class PaymentDispatcherService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_provider(
        payment_provider,
    ):

        return (
            PaymentProviderFactory.get_provider(
                payment_provider,
            )
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def initialize_payment(
        db,
        payment_reference,
    ) -> PaymentInitializationResult:

        payment = (
            PaymentService.get_payment(
                db,
                payment_reference,
            )
        )

        transaction = (

            PaymentTransactionService
            .get_or_create_transaction(

                db=db,

                payment_id=payment.payment_id,

                payment_provider=(
                    payment.payment_provider
                ),

            )

        )

        provider = (
            PaymentDispatcherService
            ._get_provider(
                payment.payment_provider,
            )
        )

        result = (
            provider.initialize_payment(
                payment,
                transaction,
            )
        )

        PaymentTransactionService.record_initialization(

            db=db,

            transaction_id=(
                transaction.transaction_id
            ),

            gateway_reference=(
                result.gateway_reference
            ),

            gateway_status=(
                result.gateway_status
            ),

            gateway_response=(
                result.gateway_response
            ),

            metadata=(
                result.metadata
            ),

        )

        return result

    @staticmethod
    def verify_payment(
        db,
        transaction_id,
    ) -> PaymentVerificationResult:

        transaction = (
            PaymentTransactionService
            .get_transaction(
                db,
                transaction_id,
            )
        )

        provider = (
            PaymentDispatcherService
            ._get_provider(
                transaction.payment.payment_provider,
            )
        )

        result = (
            provider.verify_payment(
                transaction,
            )
        )

        PaymentTransactionService.record_verification(

            db=db,

            transaction_id=(
                transaction.transaction_id
            ),

            transaction_status=(
                result.transaction_status
            ),

            gateway_transaction_id=(
                result.gateway_transaction_id
            ),

            authorization_code=(
                result.authorization_code
            ),

            paid_at=(
                result.paid_at
            ),

            gateway_status=(
                result.gateway_status
            ),

            gateway_response=(
                result.gateway_response
            ),

            metadata=(
                result.metadata
            ),

        )

        return result

    @staticmethod
    def validate_webhook(
        payment_provider,
        headers,
        body,
    ) -> PaymentValidationResult:

        provider = (
            PaymentDispatcherService
            ._get_provider(
                payment_provider,
            )
        )

        return (
            provider.validate_webhook(
                headers,
                body,
            )
        )

    @staticmethod
    def parse_webhook(
        payment_provider,
        payload,
    ) -> PaymentWebhookResult:

        provider = (
            PaymentDispatcherService
            ._get_provider(
                payment_provider,
            )
        )

        return (
            provider.parse_webhook(
                payload,
            )
        )