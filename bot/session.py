from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)

from bot.keyboards import get_main_keyboard

from bot.services.session_service import SessionService

async def render_session(
    message_obj,
    telegram_user_id,
    session=None
):

    if session is None:

        session = SessionService.get_session(
            telegram_user_id
        )

        if session is None:
            return None
        
    message = session["message"]
    keyboard = session["keyboard"]

    if keyboard == "REMOVE":

        await message_obj.reply_text(
            message,
            reply_markup=ReplyKeyboardRemove()
        )

        return session

    if keyboard == "REQUEST_PHONE":
        keyboard_markup = ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        "📱 Share Phone Number",
                        request_contact=True
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await message_obj.reply_text(
            message,
            reply_markup=keyboard_markup
        )

        return session

    if keyboard == "MAIN_MENU":

        await message_obj.reply_text(
            message,
            reply_markup=get_main_keyboard()
        )

        return session

    return session