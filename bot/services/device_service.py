import requests

from bot.config import (
    API_BASE_URL,
)


class DeviceService:

    @staticmethod
    def get_devices(
        telegram_user_id,
    ):

        response = requests.get(
            f"{API_BASE_URL}/portal/devices/"
            f"{telegram_user_id}",
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def rename_device(
        telegram_user_id,
        device_id,
        device_name,
    ):

        response = requests.patch(
            f"{API_BASE_URL}/portal/devices/"
            f"{device_id}/rename",
            json={
                "telegram_user_id": telegram_user_id,
                "device_name": device_name,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def activate_device(
        telegram_user_id,
        device_id,
    ):

        response = requests.patch(
            f"{API_BASE_URL}/portal/devices/"
            f"{device_id}/activate",
            json={
                "telegram_user_id": telegram_user_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def deactivate_device(
        telegram_user_id,
        device_id,
    ):

        response = requests.patch(
            f"{API_BASE_URL}/portal/devices/"
            f"{device_id}/deactivate",
            json={
                "telegram_user_id": telegram_user_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def block_device(
        telegram_user_id,
        device_id,
    ):

        response = requests.patch(
            f"{API_BASE_URL}/portal/devices/"
            f"{device_id}/block",
            json={
                "telegram_user_id": telegram_user_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()

    @staticmethod
    def unblock_device(
        telegram_user_id,
        device_id,
    ):

        response = requests.patch(
            f"{API_BASE_URL}/portal/devices/"
            f"{device_id}/unblock",
            json={
                "telegram_user_id": telegram_user_id,
            },
        )

        if response.status_code != 200:

            return None

        return response.json()