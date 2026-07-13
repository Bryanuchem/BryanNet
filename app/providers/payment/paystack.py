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


class PaystackProvider(
    PaymentProvider,
):

    BASE_URL = (
        "https://api.paystack.co"
    )

    SIGNATURE_HEADER = (
        "x-paystack-signature"
    )

    def __init__(
        self,
    ):

        secret_key = (
            os.getenv(
                "PAYSTACK_SECRET_KEY",
            )
        )

        if secret_key is None:

            raise RuntimeError(
                "PAYSTACK_SECRET_KEY "
                "is not configured."
            )

        self.secret_key = (
            secret_key
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
        Initialize a payment with Paystack.
        """

        payload = {

            "reference":
                payment.payment_reference,

            "email":
                payment.customer.email,

            "amount":
                int(
                    payment.amount * 100
                ),

            "metadata": {

                "customer_id":
                    payment.customer_id,

                "plan_id":
                    payment.plan_id,

            },

        }

        response = requests.post(

            (
                f"{self.BASE_URL}"
                "/transaction/initialize"
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
                data["authorization_url"]
            ),

            gateway_reference=(
                data["reference"]
            ),

            gateway_status="INITIALIZED",

            gateway_response=(
                result.get(
                    "message",
                )
            ),

            metadata={

                "access_code":
                    data["access_code"],

            },

        )

    def verify_payment(
        self,
        transaction,
    ) -> PaymentVerificationResult:
        """
        Verify a payment using Paystack.
        """

        response = requests.get(

            (
                f"{self.BASE_URL}"
                "/transaction/verify/"
                f"{transaction.gateway_reference}"
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
                == "success"
            ),

            transaction_status=(

                TransactionStatus.SUCCESSFUL

                if data["status"] == "success"

                else TransactionStatus.FAILED

            ),

            gateway_reference=(
                data["reference"]
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
                    data["amount"] / 100,

                "access_code":
                    data.get(
                        "access_code",
                    ),

            },

        )

    def validate_webhook(
        self,
        headers,
        body,
    ) -> PaymentValidationResult:

        raise NotImplementedError(
            "Paystack webhook validation "
            "has not yet been implemented."
        )

    def parse_webhook(
        self,
        payload,
    ) -> PaymentWebhookResult:

        raise NotImplementedError(
            "Paystack webhook parsing "
            "has not yet been implemented."
        )