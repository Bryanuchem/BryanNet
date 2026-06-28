import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            "60"
        )
    )

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )


settings = Settings()