from app.providers.payment.base import (
    PaymentProvider,
)


class ManualPaymentProvider(
    PaymentProvider,
):

    def initialize_payment(
        self,
        payment,
    ):
        """
        Manual payments do not require an external
        payment gateway.

        The customer completes the payment outside
        BryanNet and an administrator later confirms
        the payment.
        """

        return {

            "success": True,

            "provider": "manual",

            "payment_reference": (
                payment.payment_reference
            ),

            "message": (
                "Awaiting manual payment confirmation."
            ),

        }

    def verify_payment(
        self,
        payment_reference,
    ):
        """
        Manual payments are verified by an
        administrator.

        Calling verify_payment() completes the
        payment inside BryanNet.
        """

        raise NotImplementedError(
            "Manual payment verification must be "
            "performed by an administrator using "
            "PaymentService.complete_payment()."
        )