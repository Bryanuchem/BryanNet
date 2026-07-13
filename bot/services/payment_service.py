import requests

from bot.config import (
    API_BASE_URL,
)


class PaymentService:

    @staticmethod
    def initialize_payment(
        telegram_user_id,
        plan_id,
    ):

        response = requests.post(
            f"{API_BASE_URL}/portal/payments/initialize",
            json={
                "telegram_user_id": telegram_user_id,
                "plan_id": plan_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def get_payment(
        telegram_user_id,
        payment_reference,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/payments/"
            f"{payment_reference}",
            params={
                "telegram_user_id": telegram_user_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def get_receipt(
        telegram_user_id,
        payment_reference,
    ):

        response = requests.get(

            f"{API_BASE_URL}"
            "/portal/payments/"
            f"{payment_reference}"
            "/receipt",

            params={

                "telegram_user_id":
                    telegram_user_id,

            },

        )

        if response.status_code != 200:

            return None

        return response.content

    @staticmethod
    def verify_payment(
        payment_reference,
    ):

        response = requests.post(

            f"{API_BASE_URL}/portal/payments/{payment_reference}/verify",

        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def retry_payment(
        telegram_user_id,
        payment_reference,
    ):

        response = requests.post(

            f"{API_BASE_URL}"

            f"/portal/payments/retry/{payment_reference}",

            params={

                "telegram_user_id":
                    telegram_user_id,

            },

        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def get_payments(
        telegram_user_id,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/payments/customer/"
            f"{telegram_user_id}",
        )

        if response.status_code != 200:

            return None

        return response.json()
    
    @staticmethod
    def get_payment_details(
        payment_reference,
    ):

        response = requests.get(

            f"{API_BASE_URL}"
            "/portal/payments/details/"
            f"{payment_reference}",

        )

        if response.status_code != 200:

            return None

        return response.json()