from functools import lru_cache

from sqlalchemy.engine import URL

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # ==========================================================
    # Application
    # ==========================================================

    app_name: str = "BryanNet API"

    app_version: str = "1.0.0"

    debug: bool = False

    api_base_url: str = "http://127.0.0.1:8000/api/v1"

    api_prefix: str = "/api/v1"

    frontend_origin: str = "http://localhost:5173"

    # ==========================================================
    # Database
    # ==========================================================

    db_host: str = "localhost"

    db_port: int = 3306

    db_name: str = "bryannet"

    db_user: str = "root"

    db_password: str = ""

    # ==========================================================
    # JWT
    # ==========================================================

    jwt_secret: str = ""

    jwt_algorithm: str = "HS256"

    jwt_expire_minutes: int = 1440

    # ==========================================================
    # Router Encryption
    # ==========================================================

    router_encryption_key: str = ""
    router_username_prefix: str = "BRN"

    # ==========================================================
    # Telegram
    # ==========================================================

    portal_url: str = ""
    
    telegram_bot_token: str = ""

    telegram_bot_username: str = ""

    # ==========================================================
    # Paystack
    # ==========================================================

    paystack_public_key: str = ""

    paystack_secret_key: str =  ""
    
    payment_expiry_hours: int = 24
    
    # ==========================================================
    # Flutterwave
    # ==========================================================
    flutterwave_secret_key: str = ""

    flutterwave_webhook_secret: str = ""

    @property
    def database_url(self) -> URL:

        return URL.create(
            drivername="mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()
