from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

def get_main_keyboard(
    has_active_subscription,
):

    if has_active_subscription:

        keyboard = [

            [
                "📡 Menu",
                "📊 My Status",
            ],

            [
                "📋 View Plans",
                "🌐 Buy Internet",
            ],

            [
                "💻 My Devices",
                "💳 Payments",
            ],

            [
                "❓ Help",
            ],

        ]

    else:

        keyboard = [

            [
                "📡 Menu",
                "🌐 Buy Internet",
            ],

            [
                "📋 View Plans",
                "💳 Payments",
            ],

            [
                "❓ Help",
            ],

        ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True
    )
    
# ==========================================================
# Payments
# ==========================================================

def get_payment_checkout_keyboard(
    checkout_url,
):

    return InlineKeyboardMarkup(

        [

            [

                InlineKeyboardButton(

                    text="💳 Pay with Paystack",

                    url=checkout_url,

                ),

            ],

        ],

    )