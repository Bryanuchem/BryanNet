from telegram.ext import (
    Application
)

from bot.config import BOT_TOKEN
from bot.handlers import setup_handlers


app = (
    Application.builder()
    .token(BOT_TOKEN)
    .build()
)

setup_handlers(app)

app.run_polling()