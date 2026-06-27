import requests
from bot.config import API_BASE_URL

class CustomerService:

    @staticmethod
    def start_onboarding(telegram_user_id):
        response = requests.post(
            f"{API_BASE_URL}/customers/onboarding/start",
            json={
                "telegram_user_id": telegram_user_id
            }
        )
        return response.status_code == 200

    @staticmethod
    def update_name(telegram_user_id, full_name):
        response = requests.patch(
            f"{API_BASE_URL}/customers/onboarding/name",
            json={
                "telegram_user_id": telegram_user_id,
                "full_name": full_name
            }
        )
        return response.status_code == 200

    @staticmethod
    def update_phone(telegram_user_id, phone_number):
        response = requests.patch(
            f"{API_BASE_URL}/customers/onboarding/phone",
            json={
                "telegram_user_id": telegram_user_id,
                "phone_number": phone_number
            }
        )
        return response.status_code == 200