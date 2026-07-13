import os

import requests

from app.domain.payment import (
    PaymentInitializationResult,
    PaymentValidationResult,
    PaymentVerificationResult,
    PaymentWebhookResult,
)

from app.enums import (
    TransactionStatus,
)

from app.providers.payment.base import (
    PaymentProvider,
)


class FlutterwaveProvider(
    PaymentProvider,
):

    BASE_URL = (
        "https://api.flutterwave.com/v3"
    )

    SIGNATURE_HEADER = (
        "verif-hash"
    )

    def __init__(
        self,
    ):

        secret_key = (
            os.getenv(
                "FLUTTERWAVE_SECRET_KEY",
            )
        )

        webhook_secret = (
            os.getenv(
                "FLUTTERWAVE_WEBHOOK_SECRET",
            )
        )

        if secret_key is None:

            raise RuntimeError(
                "FLUTTERWAVE_SECRET_KEY "
                "is not configured."
            )

        if webhook_secret is None:

            raise RuntimeError(
                "FLUTTERWAVE_WEBHOOK_SECRET "
                "is not configured."
            )

        self.secret_key = (
            secret_key
        )

        self.webhook_secret = (
            webhook_secret
        )

        self.headers = {

            "Authorization":
                f"Bearer {self.secret_key}",

            "Content-Type":
                "application/json",

        }

    # ==========================================================
    # PaymentProvider Implementation
    # ==========================================================

    def initialize_payment(
        self,
        payment,
        transaction,
    ) -> PaymentInitializationResult:
        """
        Initialize a payment with Flutterwave.
        """

        payload = {

            "tx_ref":
                payment.payment_reference,

            "amount":
                float(
                    payment.amount
                ),

            "currency":
                "NGN",

            "redirect_url":
                "",

            "customer": {

                "email":
                    payment.customer.email,

            },

            "meta": {

                "customer_id":
                    payment.customer_id,

                "plan_id":
                    payment.plan_id,

            },

        }

        response = requests.post(

            (
                f"{self.BASE_URL}"
                "/payments"
            ),

            json=payload,

            headers=self.headers,

            timeout=30,

        )

        response.raise_for_status()

        result = response.json()

        data = result["data"]

        return PaymentInitializationResult(

            authorization_url=(
                data["link"]
            ),

            gateway_reference=(
                payment.payment_reference
            ),

            gateway_status="INITIALIZED",

            gateway_response=(
                result.get(
                    "message",
                )
            ),

            metadata={

                "provider":
                    "flutterwave",

            },

        )

    def verify_payment(
        self,
        transaction,
    ) -> PaymentVerificationResult:
        """
        Verify a payment using Flutterwave.
        """

        response = requests.get(

            (
                f"{self.BASE_URL}"
                "/transactions/verify_by_reference"
                f"?tx_ref={transaction.gateway_reference}"
            ),

            headers=self.headers,

            timeout=30,

        )

        response.raise_for_status()

        result = response.json()

        data = result["data"]

        return PaymentVerificationResult(

            verified=(
                data["status"]
                == "successful"
            ),

            transaction_status=(

                TransactionStatus.SUCCESSFUL

                if data["status"] == "successful"

                else TransactionStatus.FAILED

            ),

            gateway_reference=(
                data["tx_ref"]
            ),

            gateway_transaction_id=(
                str(data["id"])
            ),

            paid_at=None,

            gateway_status=(
                data["status"]
            ),

            gateway_response=(
                result.get(
                    "message",
                )
            ),

            metadata={

                "amount":
                    data["amount"],

            },

        )

    def validate_webhook(
        self,
        headers,
        body,
    ) -> PaymentValidationResult:

        raise NotImplementedError(
            "Flutterwave webhook validation "
            "has not yet been implemented."
        )

    def parse_webhook(
        self,
        payload,
    ) -> PaymentWebhookResult:

        raise NotImplementedError(
            "Flutterwave webhook parsing "
            "has not yet been implemented."
        )