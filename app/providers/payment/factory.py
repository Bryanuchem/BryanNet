from fastapi import HTTPException

from app.enums import (
    PaymentProvider,
)

from app.providers.payment.base import (
    PaymentProvider as PaymentProviderBase,
)

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

    PROVIDERS = {

        PaymentProvider.MANUAL:
            ManualPaymentProvider,

        PaymentProvider.PAYSTACK:
            PaystackProvider,

        PaymentProvider.FLUTTERWAVE:
            FlutterwaveProvider,

    }

    @staticmethod
    def get_provider(
        payment_provider: PaymentProvider,
    ) -> PaymentProviderBase:

        provider = (

            PaymentProviderFactory
            .PROVIDERS
            .get(
                payment_provider,
            )

        )

        if provider is None:

            raise HTTPException(
                status_code=500,
                detail=(
                    "Unsupported payment provider."
                ),
            )

        return provider()