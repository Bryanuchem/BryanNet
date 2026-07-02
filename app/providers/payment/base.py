from abc import (
    ABC,
    abstractmethod,
)


class PaymentProvider(
    ABC,
):

    @abstractmethod
    def initialize_payment(
        self,
        payment,
    ):
        """
        Initialize a payment with the payment gateway.

        Returns provider-specific initialization data,
        such as an authorization URL or checkout link.
        """

        raise NotImplementedError

    @abstractmethod
    def verify_payment(
        self,
        payment_reference,
    ):
        """
        Verify a payment with the payment gateway
        using BryanNet's payment reference.

        Returns provider-specific verification data.
        """

        raise NotImplementedError