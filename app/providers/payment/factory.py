from fastapi import HTTPException

from app.enums import PaymentProvider

from app.providers.payment.flutterwave import (
    FlutterwaveProvider,
)
from app.providers.payment.manual import (
    ManualPaymentProvider,
)
from app.providers.payment.paystack import (
    PaystackProvider,
)


class PaymentProviderFactory:

    @staticmethod
    def get_provider(
        payment_provider: PaymentProvider,
    ):

        if (
            payment_provider
            == PaymentProvider.PAYSTACK
        ):

            return (
                PaystackProvider()
            )

        if (
            payment_provider
            == PaymentProvider.FLUTTERWAVE
        ):

            return (
                FlutterwaveProvider()
            )

        if (
            payment_provider
            == PaymentProvider.MONNIFY
        ):

            raise NotImplementedError(
                "Monnify provider has not "
                "been implemented yet."
            )

        if (
            payment_provider
            == PaymentProvider.MANUAL
        ):

            return (
                ManualPaymentProvider()
            )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unsupported payment provider."
            ),
        )