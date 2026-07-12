import requests

from bot.config import (
    API_BASE_URL,
)


class PlanService:

    @staticmethod
    def get_all_plans():

        response = requests.get(
            f"{API_BASE_URL}/portal/plans",
        )

        if response.status_code != 200:

            return None

        return response.json()