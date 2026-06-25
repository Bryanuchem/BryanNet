from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

def get_main_keyboard():

    keyboard = [

        [
            "📊 My Status",
            "🌐 Buy Internet"
        ],

        [
            "💻 My Devices",
            "📋 View Plans"
        ],

        [
            "❌ Remove Device",
            "📡 Menu"
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True
    )

def get_inline_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "📊 My Status",
                callback_data="status"
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 Buy Internet",
                callback_data="buy"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 View Plans",
                callback_data="plans"
            )
        ],

        [
            InlineKeyboardButton(
                "💻 My Devices",
                callback_data="devices"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ Remove Device",
                callback_data="remove_device"
            )
        ]

    ]

    return InlineKeyboardMarkup(
        keyboard
    )
   