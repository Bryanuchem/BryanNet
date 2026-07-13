from app.domain.payment import (
    PaymentInitializationResult,
    PaymentValidationResult,
    PaymentVerificationResult,
    PaymentWebhookResult,
)

from app.enums import (
    TransactionStatus,
)

from .base import (
    PaymentProvider,
)


class ManualPaymentProvider(
    PaymentProvider,
):

    def initialize_payment(
        self,
        payment,
        transaction,
    ) -> PaymentInitializationResult:

        return PaymentInitializationResult(

            gateway_reference=(
                transaction.gateway_reference
            ),

            gateway_status="MANUAL",

            gateway_response=(
                "Manual payment initialized."
            ),

        )

    def verify_payment(
        self,
        transaction,
    ) -> PaymentVerificationResult:

        return PaymentVerificationResult(

            verified=True,

            transaction_status=(
                TransactionStatus.SUCCESSFUL
            ),

            gateway_reference=(
                transaction.gateway_reference
            ),

            gateway_status="SUCCESS",

            gateway_response=(
                "Manual payment verified."
            ),

        )

    def validate_webhook(
        self,
        headers,
        body,
    ) -> PaymentValidationResult:

        return PaymentValidationResult(

            valid=True,

            message=(
                "Manual payments do not "
                "require webhook validation."
            ),

        )

    def parse_webhook(
        self,
        payload,
    ) -> PaymentWebhookResult:

        return PaymentWebhookResult(

            valid=True,

            event="manual.payment",

            gateway_reference=None,

        )