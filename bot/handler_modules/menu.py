from telegram import (
    Update,
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from bot.session import (
    render_session,
)

# ==========================================================
# Commands
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await render_session(
        update.message,
        update.effective_user.id,
    )


async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = (
        "🛰 BryanNet Assistant\n\n"
        "Choose an option below to get started.\n\n"

        "📊 My Status\n"
        "View your active subscription and connection.\n\n"

        "📋 View Plans\n"
        "Browse all available internet plans.\n\n"

        "🌐 Buy Internet\n"
        "Purchase a new internet plan.\n\n"

        "💻 My Devices\n"
        "View and manage your registered devices.\n\n"

        "❓ Help\n"
        "Get help and contact support."
    )

    await update.message.reply_text(
        text,
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