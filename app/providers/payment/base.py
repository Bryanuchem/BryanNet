from abc import (
    ABC,
    abstractmethod,
)

from app.domain.payment import (
    PaymentInitializationResult,
    PaymentValidationResult,
    PaymentVerificationResult,
    PaymentWebhookResult,
)


class PaymentProvider(
    ABC,
):

    @abstractmethod
    def initialize_payment(
        self,
        payment,
        transaction,
    ) -> PaymentInitializationResult:
        """
        Initialize a payment with the payment provider.
        """

        raise NotImplementedError

    @abstractmethod
    def verify_payment(
        self,
        transaction,
    ) -> PaymentVerificationResult:
        """
        Verify a payment transaction with the payment provider.
        """

        raise NotImplementedError

    @abstractmethod
    def validate_webhook(
        self,
        headers,
        body,
    ) -> PaymentValidationResult:
        """
        Validate an incoming webhook request.
        """

        raise NotImplementedError

    @abstractmethod
    def parse_webhook(
        self,
        payload,
    ) -> PaymentWebhookResult:
        """
        Parse a validated webhook payload into
        BryanNet's domain model.
        """

        raise NotImplementedError