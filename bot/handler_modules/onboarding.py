from telegram import (
    Update,
)

from telegram.ext import (
    ContextTypes,
)

from bot.session import (
    render_session,
)

from bot.services.onboarding_service import (
    OnboardingService,
)

from bot.services.session_service import (
    SessionService,
)

from bot.handler_modules.payment import (
    payment_return,
)

async def onboarding_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    telegram_user_id = (
        update.effective_user.id
    )

    # ======================================================
    # Payment Deep Link
    # ======================================================

    if context.args:

        payload = (
            context.args[0]
        )

        if payload.startswith(
            "payment_",
        ):

            payment_reference = (
                payload.removeprefix(
                    "payment_",
                )
            )

            await payment_return(

                update=update,

                context=context,

                payment_reference=(
                    payment_reference
                ),

            )

            return

    session = (
        SessionService.get_session(
            telegram_user_id,
        )
    )

    if session is None:

        return

    next_action = session[
        "next_action"
    ]

    # ======================================================
    # Customer already onboarded
    # ======================================================

    if next_action == "SHOW_MAIN_MENU":

        return

    # ======================================================
    # Start onboarding
    # ======================================================

    if next_action == "START_ONBOARDING":

        success = (
            OnboardingService.start_onboarding(
                telegram_user_id,
            )
        )

        if not success:

            await update.message.reply_text(
                "Unable to start onboarding.",
            )

            return

        await render_session(
            update.message,
            telegram_user_id,
        )

        return

    # ======================================================
    # Save full name
    # ======================================================

    if next_action == "ENTER_NAME":

        if not update.message.text:

            return

        success = (
            OnboardingService.update_name(
                telegram_user_id,
                update.message.text.strip(),
            )
        )

        if not success:

            await update.message.reply_text(
                "Unable to save your name.",
            )

            return

        await render_session(
            update.message,
            telegram_user_id,
        )

        return

    # ======================================================
    # Save phone number
    # ======================================================

    if next_action == "ENTER_PHONE_NUMBER":

        if update.message.contact is None:

            await update.message.reply_text(
                "Please tap "
                "'📱 Share Phone Number'.",
            )

            return

        success = (
            OnboardingService.update_phone(
                telegram_user_id,
                update.message.contact.phone_number,
            )
        )

        if not success:

            await update.message.reply_text(
                "Unable to save your phone number.",
            )

            return

        session = (
            SessionService.get_session(
                telegram_user_id,
                first_login=True,
            )
        )

        if session is None:

            await update.message.reply_text(
                "Unable to retrieve your session.",
            )

            return

        await render_session(
            update.message,
            telegram_user_id,
            session=session,
        )
        
    # ======================================================
    # Save email
    # ======================================================

    if next_action == "ENTER_EMAIL":

        if not update.message.text:

            await update.message.reply_text(
                "Please enter your email address.",
            )

            return

        email = (
            update.message.text
            .strip()
            .lower()
        )

        success = (
            OnboardingService.update_email(
                telegram_user_id,
                email,
            )
        )

        if not success:

            await update.message.reply_text(
                "Unable to save your email.",
            )

            return

        session = (
            SessionService.get_session(
                telegram_user_id,
                first_login=True,
            )
        )

        if session is None:

            await update.message.reply_text(
                "Unable to retrieve your session.",
            )

            return

        await render_session(
            update.message,
            telegram_user_id,
            session=session,
        )

        return