import requests

from bot.config import API_BASE_URL


class SessionService:

    @staticmethod
    def get_session(
        telegram_user_id,
        first_login=False
    ):

        response = requests.get(
            f"{API_BASE_URL}/session/telegram/{telegram_user_id}",
            params={
                "first_login": first_login
            }
        )

        if response.status_code != 200:
            return None

        return response.json()