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
    # Router Events
    # ==========================================================

    router_event_url: str = (
        "http://192.168.1.116:8000/api/v1/router-events"
    )
    
    portal_login_url: str = (
        "http://192.168.1.116:8000/api/v1/portal/login"
    )
        
    portal_backend_host: str = (
        "192.168.1.116"
    )

    portal_backend_port: int = 8000
    
    portal_base_url: str = (
        "http://192.168.1.116:8000"
    )
    
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


    # ==========================================================
    # Company
    # ==========================================================

    company_name: str = "BryanNet"

    company_tagline: str = (
        "Fast • Reliable • Unlimited Internet"
    )

    company_logo_url: str = "/static/logo.svg"

    company_favicon_url: str = "/static/favicon.ico"

    support_phone: str = ""

    support_email: str = ""

    support_whatsapp: str = ""

    support_telegram: str = ""


    @property
    def portal_connected_url(self) -> str:

        return (
            
            f"http://{self.portal_backend_host}:"
        
            f"{self.portal_backend_port}"
        
            "/api/v1/portal/connected"
    
        )

    @property
    def portal_logout_url(self) -> str:

        return (
            
            f"http://{self.portal_backend_host}:"
            
            f"{self.portal_backend_port}"
            
            "/api/v1/portal/logout"
            
        )
    
        
@lru_cache
def get_settings():

    return Settings()


settings = get_settings()
