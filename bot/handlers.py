from telegram import (
    Update,
)

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.handler_modules.menu import (
    start,
    menu,
    show_help,
    cancel,
)

from bot.handler_modules.onboarding import (
    onboarding_handler,
)

from bot.handler_modules.subscriptions import (
    plans,
    send_plans,
    status,
    send_status,
    buy_keyboard,
    buy_callback,
    confirm_purchase_callback,
    cancel_purchase_callback,
)

from bot.handler_modules.devices import (
    devices,
    send_devices,
    device_callback,
    rename_device_start,
    rename_device_finish,
    activate_device,
    deactivate_device,
    block_device,
    unblock_device,
    back_to_devices,
)


# ==========================================================
# Keyboard Handler
# ==========================================================

async def keyboard_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if context.user_data.get(
        "awaiting_device_name",
    ):

        await rename_device_finish(
            update,
            context,
        )

        return

    text = update.message.text

    if text == "📊 My Status":

        await send_status(
            update.message,
            update.effective_user.id,
        )

    elif text == "📋 View Plans":

        await send_plans(
            update.message,
        )

    elif text == "🌐 Buy Internet":

        await buy_keyboard(
            update,
        )

    elif text == "💻 My Devices":

        await send_devices(
            update.message,
            update.effective_user.id,
        )

    elif text == "📡 Menu":

        await menu(
            update,
            context,
        )

    elif text == "❓ Help":

        await show_help(
            update.message,
        )


# ==========================================================
# Handler Registration
# ==========================================================

def setup_handlers(
    app,
):

    # ------------------------------------------------------
    # Commands
    # ------------------------------------------------------

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "menu",
            menu,
        )
    )

    app.add_handler(
        CommandHandler(
            "plans",
            plans,
        )
    )

    app.add_handler(
        CommandHandler(
            "status",
            status,
        )
    )
    
    # ------------------------------------------------------
    # Callback Queries
    # ------------------------------------------------------

    app.add_handler(
        CallbackQueryHandler(
            buy_callback,
            pattern="^buy_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            confirm_purchase_callback,
            pattern="^confirm_purchase$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cancel_purchase_callback,
            pattern="^cancel_purchase$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            device_callback,
            pattern="^device_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            rename_device_start,
            pattern="^rename_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            activate_device,
            pattern="^activate_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            deactivate_device,
            pattern="^deactivate_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            block_device,
            pattern="^block_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            unblock_device,
            pattern="^unblock_",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            back_to_devices,
            pattern="^devices$",
        )
    )

    # ------------------------------------------------------
    # Message Handlers
    # ------------------------------------------------------

    app.add_handler(

        MessageHandler(

            (
                filters.TEXT
                |
                filters.CONTACT
            )
            &
            ~filters.COMMAND,

            onboarding_handler,

        ),

        group=0,

    )

    app.add_handler(

        MessageHandler(

            filters.TEXT
            &
            ~filters.COMMAND,

            keyboard_handler,

        ),

        group=1,

    )