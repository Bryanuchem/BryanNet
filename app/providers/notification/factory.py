from fastapi import HTTPException

from app.providers.notification.email import (
    EmailNotificationProvider,
)

from app.providers.notification.sms import (
    SMSNotificationProvider,
)

from app.providers.notification.telegram import (
    TelegramNotificationProvider,
)


class NotificationProviderFactory:

    _providers = {

        "telegram":
            TelegramNotificationProvider,

        "email":
            EmailNotificationProvider,

        "sms":
            SMSNotificationProvider,

    }

    # ==========================================================
    # Factory
    # ==========================================================

    @classmethod
    def get_provider(
        cls,
        provider,
    ):

        provider_class = (
            cls._providers.get(
                provider.lower(),
            )
        )

        if not provider_class:

            raise HTTPException(

                status_code=400,

                detail=(
                    f"Unsupported notification "
                    f"provider: {provider}"
                ),

            )

        return provider_class()

    # ==========================================================
    # Query Methods
    # ==========================================================

    @classmethod
    def supported_providers(
        cls,
    ):

        return list(
            cls._providers.keys()
        )

    @classmethod
    def is_supported(
        cls,
        provider,
    ):

        return (
            provider.lower()
            in cls._providers
        )