import os

import requests

from app.providers.payment.base import (
    PaymentProvider,
)


from app.services.payment_dispatcher_service import (
    PaymentDispatcherService,
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

        self.secret_key: str = (
            secret_key
        )

        self.headers: dict[str, str] = {

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
    ):
        """
        Initialize a payment with Paystack.

        Returns the checkout details required
        for the customer to complete payment.
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

        result = (
            response.json()
        )

        data = (
            result["data"]
        )

        return {

            "authorization_url":
                data["authorization_url"],

            "access_code":
                data["access_code"],

            "reference":
                data["reference"],

        }

    def verify_payment(
        self,
        payment_reference,
    ):
        """
        Verify a payment using Paystack's
        Verify Transaction endpoint.

        Returns a standardized verification
        response for BryanNet.
        """

        response = requests.get(

            (
                f"{self.BASE_URL}"
                "/transaction/verify/"
                f"{payment_reference}"
            ),

            headers=self.headers,

            timeout=30,

        )

        response.raise_for_status()

        result = (
            response.json()
        )

        data = (
            result["data"]
        )

        return {

            "verified":
                data["status"]
                == "success",

            "payment_reference":
                data["reference"],

            "gateway_transaction_id":
                str(
                    data["id"]
                ),

            "amount":
                data["amount"] / 100,

            "provider":
                "paystack",

        }
        
    # ==========================================================
    # Webhook Helpers
    # ==========================================================

    def verify_signature(
        self,
        payload,
        signature,
    ):
        """
        Verify the Paystack webhook signature.

        This should be called by the webhook
        endpoint before processing the payload.
        """

        import hashlib
        import hmac
        import json

        expected_signature = (
            hmac.new(

                self.secret_key.encode(
                    "utf-8",
                ),

                json.dumps(
                    payload,
                    separators=(",", ":"),
                ).encode(
                    "utf-8",
                ),

                hashlib.sha512,

            ).hexdigest()
        )

        return hmac.compare_digest(
            expected_signature,
            signature,
        )

    def process_webhook(
        self,
        db,
        payload,
    ):
        """
        Process a trusted Paystack webhook.

        Assumes the webhook signature has
        already been verified.
        """

        event = payload.get(
            "event",
        )

        if event != "charge.success":

            return {

                "processed": False,

                "message":
                    "Webhook ignored.",

            }

        data = payload.get(
            "data",
            {},
        )

        payment_reference = (
            data.get(
                "reference",
            )
        )

        if not payment_reference:

            raise ValueError(
                "Payment reference missing "
                "from webhook payload."
            )

        return (
            PaymentDispatcherService
            .verify_payment(
                db=db,
                payment_reference=payment_reference,
            )
        )        