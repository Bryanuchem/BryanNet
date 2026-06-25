import requests

from telegram import Update

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from bot.config import API_BASE_URL

REGISTER_NAME = 1
REGISTER_PHONE = 2

async def register_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "What is your full name?"
    )

    return REGISTER_NAME

async def register_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["full_name"] = (
        update.message.text
    )

    await update.message.reply_text(
        "What is your phone number?"
    )

    return REGISTER_PHONE

async def register_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    phone_number = (
        update.message.text
    )

    full_name = (
        context.user_data["full_name"]
    )

    telegram_user_id = (
        update.effective_user.id
    )

    response = requests.post(
        f"{API_BASE_URL}/customers/register",
        json={
            "phone_number": phone_number,
            "full_name": full_name,
            "telegram_user_id": telegram_user_id
        }
    )

    if response.status_code == 200:

        await update.message.reply_text(
            "Registration successful."
        )

    else:

        await update.message.reply_text(
            "Registration failed."
        )

    return ConversationHandler.END

async def register_cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Registration cancelled."
    )

    return ConversationHandler.END
