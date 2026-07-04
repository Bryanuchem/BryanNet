from telegram import (
    Update
)

from telegram.ext import (
    ContextTypes
)

from bot.session import render_session
from bot.services.customer_service import CustomerService
from bot.services.session_service import SessionService

async def onboarding_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_user_id = update.effective_user.id

    session = SessionService.get_session(
        telegram_user_id
    )

    if session is None:
        return

    next_action = session["next_action"]

    # Customer is already fully onboarded.
    # Let the normal keyboard handler process the message.

    if next_action == "SHOW_MAIN_MENU":
        return

    # Save customer's full name

    if next_action == "ENTER_NAME":

        if not update.message.text:
            return

        success = CustomerService.update_name(
            telegram_user_id,
            update.message.text
        )

        if not success:

            await update.message.reply_text(
                "Unable to save your name."
            )

            return

        await render_session(
            update.message,
            telegram_user_id
        )

        return

    # Save customer's phone number

    elif next_action == "ENTER_PHONE":

        if update.message.contact is None:

            await update.message.reply_text(
                "Please tap '📱 Share Phone Number'."
            )

            return

        success = CustomerService.update_phone(
            telegram_user_id,
            update.message.contact.phone_number
        )

        if not success:

            await update.message.reply_text(
                "Unable to save your phone number."
            )

            return

        session = SessionService.get_session(
            telegram_user_id,
            first_login=True
        )

        if session is None:

            await update.message.reply_text(
                "Unable to retrieve your session."
            )

            return

        await render_session(
            update.message,
            telegram_user_id,
            session=session
        )

        return