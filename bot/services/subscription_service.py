import requests

from bot.config import (
    API_BASE_URL,
)


class SubscriptionService:

    @staticmethod
    def get_subscription_status(
        telegram_user_id,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/subscriptions/"
            f"{telegram_user_id}",
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def get_subscriptions(
        telegram_user_id,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/subscriptions/"
            f"{telegram_user_id}",
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def get_subscription(
        telegram_user_id,
        subscription_id,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/subscriptions/"
            f"{telegram_user_id}/"
            f"{subscription_id}",
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def purchase_subscription(
        telegram_user_id,
        payment_reference,
    ):

        response = requests.post(
            f"{API_BASE_URL}/portal/subscriptions",
            json={
                "telegram_user_id": telegram_user_id,
                "payment_reference": payment_reference,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()