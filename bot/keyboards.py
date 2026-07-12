from telegram import (
    ReplyKeyboardMarkup,
)

def get_main_keyboard():
    keyboard = [
        [
            "📊 My Status",
            "📋 View Plans"
        ],
        [
            "🌐 Buy Internet",
            "💻 My Devices"
        ],
        [
            "📡 Menu",
            "❓ Help",  
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True
    )