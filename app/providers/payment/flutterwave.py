import os

import hmac

import requests

from app.providers.payment.base import (
    PaymentProvider,
)

from app.services.payment_dispatcher_service import (
    PaymentDispatcherService,
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

        self.secret_key: str = (
            secret_key
        )

        self.webhook_secret: str = (
            webhook_secret
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
        Initialize a payment with Flutterwave.

        Returns the checkout link required
        for the customer to complete payment.
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

        result = (
            response.json()
        )

        data = (
            result["data"]
        )

        return {

            "checkout_url":
                data["link"],

            "reference":
                payment.payment_reference,

        }

    def verify_payment(
        self,
        payment_reference,
    ):
        """
        Verify a payment with Flutterwave.

        Returns a standardized verification
        response for BryanNet.
        """

        response = requests.get(

            (
                f"{self.BASE_URL}"
                "/transactions/verify_by_reference"
                f"?tx_ref={payment_reference}"
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
                == "successful",

            "payment_reference":
                data["tx_ref"],

            "gateway_transaction_id":
                str(
                    data["id"]
                ),

            "amount":
                data["amount"],

            "provider":
                "flutterwave",

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
        Verify the Flutterwave webhook.

        Flutterwave sends the webhook secret
        directly in the signature header.
        """

        return hmac.compare_digest(

            signature,

            self.webhook_secret,

        )

    def process_webhook(
        self,
        db,
        payload,
    ):
        """
        Process a trusted Flutterwave webhook.

        Assumes the webhook signature has
        already been verified.
        """

        event = payload.get(
            "event",
        )

        if event != "charge.completed":

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
                "tx_ref",
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