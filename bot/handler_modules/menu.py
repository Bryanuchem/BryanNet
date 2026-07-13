from telegram import (
    Update,
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from app.enums.next_action import (
    NextAction,
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

from bot.session import (
    render_session,
)

from bot.keyboards import (
    get_main_keyboard,
)

# ==========================================================
# Commands
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    
    if context.args:

        payload = (
            context.args[0]
        )

        if payload.startswith(
            "payment_",
        ):
            
            await payment_return(

                update=update,

                context=context,

                payment_reference=(

                    payload.removeprefix(
                        "payment_",
                    )

                ),

            )
            return

    telegram_user_id = (
        update.effective_user.id
    )

    session = (
        SessionService.get_session(
            telegram_user_id,
        )
    )

    if session is None:

        await update.message.reply_text(
            "Unable to start your session.",
        )

        return

    if (
        session["next_action"]
        == NextAction.START_ONBOARDING.value
    ):

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


async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = (

        "🛰 BryanNet Assistant\n\n"

        "Choose an option below.\n\n"

        "📊 My Status\n"
        "View your active subscription and connection.\n\n"

        "📋 View Plans\n"
        "Browse all available internet plans.\n\n"

        "🌐 Buy Internet\n"
        "Purchase a new internet plan.\n\n"

        "💻 My Devices\n"
        "View and manage your registered devices.\n\n"

        "💳 Payments\n"
        "View your payment history and receipts.\n\n"

        "❓ Help\n"
        "Get help and contact support."

    )

    telegram_user_id = (
        update.effective_user.id
    )

    session = (
        SessionService.get_session(
            telegram_user_id,
        )
    )

    message = (
        update.effective_message
    )

    await message.reply_text(

        text,

        reply_markup=(
            get_main_keyboard(
                session[
                    "has_active_subscription"
                ],
            )
        ),

    )

async def show_help(
    message,
):

    await message.reply_text(

        "❓ BryanNet Help\n\n"

        "Available commands:\n\n"

        "📊 My Status\n"
        "Check your current subscription.\n\n"

        "📋 View Plans\n"
        "See all available internet plans.\n\n"

        "🌐 Buy Internet\n"
        "Purchase a new subscription.\n\n"

        "💻 My Devices\n"
        "Manage your registered devices.\n\n"

        "If you need further assistance, "
        "please contact BryanNet support.",

    )


# ==========================================================
# Conversation
# ==========================================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        "Operation cancelled.",
    )

    return ConversationHandler.END