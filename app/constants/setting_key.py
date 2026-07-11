class SettingKeys:

    # ==========================================================
    # General
    # ==========================================================

    PLATFORM_NAME = "platform_name"

    COMPANY_NAME = "company_name"

    COMPANY_EMAIL = "company_email"

    COMPANY_PHONE = "company_phone"

    COMPANY_ADDRESS = "company_address"

    COMPANY_WEBSITE = "company_website"

    DEFAULT_TIMEZONE = "default_timezone"

    DEFAULT_CURRENCY = "default_currency"

    DATE_FORMAT = "date_format"

    TIME_FORMAT = "time_format"


    # ==========================================================
    # Authentication
    # ==========================================================

    REGISTRATION_ENABLED = "registration_enabled"

    SESSION_TIMEOUT_MINUTES = "session_timeout_minutes"

    MAX_LOGIN_ATTEMPTS = "max_login_attempts"

    PASSWORD_MIN_LENGTH = "password_min_length"

    REQUIRE_SPECIAL_CHARACTERS = "require_special_characters"

    REQUIRE_UPPERCASE = "require_uppercase"

    REQUIRE_NUMBERS = "require_numbers"

    TWO_FACTOR_AUTH_ENABLED = "two_factor_auth_enabled"


    # ==========================================================
    # Notifications
    # ==========================================================

    EMAIL_NOTIFICATIONS = "email_notifications"

    SMS_NOTIFICATIONS = "sms_notifications"

    PAYMENT_REMINDERS = "payment_reminders"

    OUTAGE_ALERTS = "outage_alerts"

    LOW_BALANCE_ALERTS = "low_balance_alerts"


    # ==========================================================
    # Network
    # ==========================================================

    DEFAULT_ROUTER = "default_router"

    DNS_PRIMARY = "dns_primary"

    DNS_SECONDARY = "dns_secondary"

    DHCP_LEASE_TIME = "dhcp_lease_time"

    BANDWIDTH_UNIT = "bandwidth_unit"


    # ==========================================================
    # Billing
    # ==========================================================

    DEFAULT_PAYMENT_METHOD = "default_payment_method"

    DEFAULT_PAYMENT_CHANNEL = "default_payment_channel"

    AUTO_SUSPEND_OVERDUE = "auto_suspend_overdue"

    SUSPEND_AFTER_DAYS = "suspend_after_days"

    INVOICE_DUE_DAYS = "invoice_due_days"

    TAX_PERCENTAGE = "tax_percentage"


    # ==========================================================
    # Integrations
    # ==========================================================

    SMTP_HOST = "smtp_host"

    SMTP_PORT = "smtp_port"

    SMTP_USERNAME = "smtp_username"

    SMTP_PASSWORD = "smtp_password"

    SMTP_USE_TLS = "smtp_use_tls"

    SMS_PROVIDER = "sms_provider"

    SMS_API_KEY = "sms_api_key"


    # ==========================================================
    # Branding
    # ==========================================================

    LOGO_URL = "logo_url"

    PRIMARY_COLOR = "primary_color"

    SECONDARY_COLOR = "secondary_color"

    LOGIN_PAGE_TITLE = "login_page_title"

    LOGIN_PAGE_SUBTITLE = "login_page_subtitle"

    FAVICON_URL = "favicon_url"


    # ==========================================================
    # System
    # ==========================================================

    MAINTENANCE_MODE = "maintenance_mode"

    DEBUG_MODE = "debug_mode"

    SYSTEM_TIMEZONE = "system_timezone"

    AUDIT_LOG_RETENTION_DAYS = "audit_log_retention_days"

    BACKUP_RETENTION_DAYS = "backup_retention_days"