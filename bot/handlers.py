from bot.handler_modules.registration import (
    REGISTER_NAME,
    REGISTER_PHONE,
    register_start,
    register_name,
    register_phone,
    register_cancel
)

from bot.handler_modules.menu import (
    start,
    menu,
    menu_callback
)

from bot.handler_modules.subscriptions import (
    BUY_PLAN,
    CONFIRM_PURCHASE,
    plans,
    send_plans,
    status,
    send_status,
    buy_start,
    buy_plan_selection,
    confirm_purchase,
    buy_keyboard
)

from bot.handler_modules.devices import (
    REMOVE_DEVICE,
    CONFIRM_REMOVE_DEVICE,
    devices,
    send_devices,
    remove_device_keyboard,
    remove_device_start,
    remove_device_selection,
    confirm_remove_device
)

from telegram import Update


from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters
)

async def keyboard_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "📊 My Status":
        await send_status(
            update.message,
            update.effective_user.id
        )

    elif text == "📋 View Plans":
        await send_plans(
            update.message
        )

    elif text == "💻 My Devices":
        await send_devices(
            update.message,
            update.effective_user.id
        )
    elif text == "🌐 Buy Internet":

        await buy_keyboard(
            update
        )
    
    elif text == "❌ Remove Device":

        await remove_device_keyboard(
            update
        )
            
    elif text == "📡 Menu":
        await menu(
            update,
            context
        )
        


def register_handlers(app):

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )
    
    app.add_handler(
        CommandHandler(
            "menu",
            menu
        )
    )
        
    app.add_handler(
        CommandHandler(
            "plans",
            plans
        )
    )
    
    registration_handler = (
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    "register",
                    register_start
                )
            ],
            states={
                REGISTER_NAME: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        register_name
                    )
                ],
                REGISTER_PHONE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        register_phone
                    )
                ]
            },
            fallbacks=[
                CommandHandler(
                    "cancel",
                    register_cancel
                )
            ]
        )
    )

    app.add_handler(
        registration_handler
    )   
    
    app.add_handler(
    CommandHandler(
        "status",
        status
    )
)
    
    app.add_handler(
    CommandHandler(
        "devices",
        devices
    )
)
    
    remove_device_handler = (
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    "remove_device",
                    remove_device_start
                )
            ],
            states={
                REMOVE_DEVICE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        remove_device_selection
                    )
                ],
                CONFIRM_REMOVE_DEVICE: [
                    MessageHandler(
                        filters.TEXT
                        & ~filters.COMMAND,
                        confirm_remove_device
                    )
                ]
            },
            fallbacks=[
                CommandHandler(
                    "cancel",
                    register_cancel
                )
            ]
        )
    )

    app.add_handler(
        remove_device_handler
    )
    
    buy_handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "buy",
                buy_start
            )
        ],
        states={
            BUY_PLAN: [
                MessageHandler(
                    filters.TEXT
                    & ~filters.COMMAND,
                    buy_plan_selection
                )
            ],
            CONFIRM_PURCHASE: [
                MessageHandler(
                    filters.TEXT
                    & ~filters.COMMAND,
                    confirm_purchase
                )
            ]            
        },
        fallbacks=[
            CommandHandler(
                "cancel",
                register_cancel
            )
        ]
    )

    app.add_handler(
        buy_handler
    )
    
    app.add_handler(
        CallbackQueryHandler(
            menu_callback
        )
    )
    
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            keyboard_handler
        )
    )