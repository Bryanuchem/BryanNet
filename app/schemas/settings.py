from pydantic import BaseModel


# ==========================================================
# Common
# ==========================================================

class SettingResponse(BaseModel):

    setting_id: int

    category: str

    key: str

    value: str

    value_type: str

    description: str | None

    is_editable: bool

    class Config:

        from_attributes = True


class SettingUpdateRequest(BaseModel):

    value: str


# ==========================================================
# General
# ==========================================================

class GeneralSettingsUpdate(BaseModel):

    platform_name: str

    company_name: str

    company_email: str

    company_phone: str

    company_address: str

    company_website: str

    default_timezone: str

    default_currency: str

    date_format: str

    time_format: str


# ==========================================================
# Authentication
# ==========================================================

class AuthenticationSettingsUpdate(BaseModel):

    registration_enabled: bool

    session_timeout_minutes: int

    max_login_attempts: int

    password_min_length: int

    require_special_characters: bool

    require_uppercase: bool

    require_numbers: bool

    two_factor_auth_enabled: bool


# ==========================================================
# Notifications
# ==========================================================

class NotificationSettingsUpdate(BaseModel):

    email_notifications: bool

    sms_notifications: bool

    payment_reminders: bool

    outage_alerts: bool

    low_balance_alerts: bool


# ==========================================================
# Network
# ==========================================================

class NetworkSettingsUpdate(BaseModel):

    default_router: str

    dns_primary: str

    dns_secondary: str

    dhcp_lease_time: int

    bandwidth_unit: str


# ==========================================================
# Billing
# ==========================================================

class BillingSettingsUpdate(BaseModel):

    default_payment_method: str

    default_payment_channel: str

    auto_suspend_overdue: bool

    suspend_after_days: int

    invoice_due_days: int

    tax_percentage: float


# ==========================================================
# Integrations
# ==========================================================

class IntegrationSettingsUpdate(BaseModel):

    smtp_host: str

    smtp_port: int

    smtp_username: str

    smtp_password: str

    smtp_use_tls: bool

    sms_provider: str

    sms_api_key: str


# ==========================================================
# Branding
# ==========================================================

class BrandingSettingsUpdate(BaseModel):

    logo_url: str

    primary_color: str

    secondary_color: str

    login_page_title: str

    login_page_subtitle: str

    favicon_url: str


# ==========================================================
# System
# ==========================================================

class SystemSettingsUpdate(BaseModel):

    maintenance_mode: bool

    debug_mode: bool

    system_timezone: str

    audit_log_retention_days: int

    backup_retention_days: int