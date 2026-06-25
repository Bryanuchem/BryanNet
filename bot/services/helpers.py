import requests

from datetime import datetime

from bot.config import API_BASE_URL

def get_customer_by_telegram_id(
    telegram_user_id
):

    response = requests.get(
        f"{API_BASE_URL}/customers/telegram/"
        f"{telegram_user_id}"
    )

    if response.status_code != 200:
        return None

    return response.json()

def get_all_plans():

    response = requests.get(
        f"{API_BASE_URL}/plans"
    )

    if response.status_code != 200:
        return None

    return response.json()

def format_duration(
    duration
):

    if duration == 0:
        return "1 Hour"

    if duration == 1:
        return "1 Day"

    return f"{duration} Days"

def format_expiry_date(
    expiry_date
):

    if not expiry_date:
        return "N/A"

    return (
        datetime
        .fromisoformat(
            expiry_date
        )
        .strftime(
            "%d %b %Y %H:%M"
        )
    )