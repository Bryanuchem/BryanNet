from fastapi import HTTPException

from app.models.setting import Setting


class SettingService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_setting(
        db,
        key,
        required=False,
    ):

        setting = (
            db.query(Setting)
            .filter(
                Setting.key == key,
            )
            .first()
        )

        if required and setting is None:

            raise HTTPException(
                status_code=404,
                detail="Setting not found.",
            )

        return setting

    @staticmethod
    def _validate_setting_key(
        key,
    ):

        if not key:

            raise HTTPException(
                status_code=400,
                detail="Setting key cannot be empty.",
            )

    @staticmethod
    def _create_setting(
        db,
        *,
        category,
        key,
        value,
        description=None,
        is_editable=True,
    ):

        setting = Setting(

            category=category,

            key=key,

            value=str(value),

            value_type=SettingService._infer_value_type(
                value,
            ),

            description=description,

            is_editable=is_editable,

        )

        db.add(
            setting,
        )

        return setting

    @staticmethod
    def _update_setting(
        setting,
        *,
        category,
        value,
        description=None,
        is_editable=True,
    ):

        setting.category = category

        setting.value = str(
            value,
        )

        setting.value_type = (
            SettingService
            ._infer_value_type(
                value,
            )
        )

        setting.description = (
            description
        )

        setting.is_editable = (
            is_editable
        )

        return setting

    @staticmethod
    def _infer_value_type(
        value,
    ):

        if isinstance(
            value,
            bool,
        ):

            return "boolean"

        if isinstance(
            value,
            int,
        ):

            return "integer"

        if isinstance(
            value,
            float,
        ):

            return "float"

        return "string"

    @staticmethod
    def _cast_value(
        value,
        value_type,
    ):

        if value is None:

            return None

        if value_type == "boolean":

            return (
                str(value).lower()
                == "true"
            )

        if value_type == "integer":

            try:

                return int(value)

            except (
                TypeError,
                ValueError,
            ):

                return 0

        if value_type == "float":

            try:

                return float(value)

            except (
                TypeError,
                ValueError,
            ):

                return 0.0

        return value

    @staticmethod
    def _get_category_defaults(
        category,
    ):

        defaults = {

            "general": {

                "platform_name": "",

                "company_name": "",

                "company_email": "",

                "company_phone": "",

                "company_address": "",

                "company_website": "",

                "default_timezone": "UTC",

                "default_currency": "NGN",

                "date_format": "DD/MM/YYYY",

                "time_format": "24 Hour",

            },

            "authentication": {

                "registration_enabled": False,

                "session_timeout_minutes": 30,

                "max_login_attempts": 5,

                "password_min_length": 8,

                "require_special_characters": True,

                "require_uppercase": True,

                "require_numbers": True,

                "two_factor_auth_enabled": False,

            },

            "notifications": {

                "email_notifications": True,

                "sms_notifications": False,

                "payment_reminders": True,

                "outage_alerts": True,

                "low_balance_alerts": True,

            },

            "network": {

                "default_router": "",

                "dns_primary": "",

                "dns_secondary": "",

                "dhcp_lease_time": 24,

                "bandwidth_unit": "Mbps",

            },

            "billing": {

                "default_payment_method": "",

                "default_payment_channel": "",

                "auto_suspend_overdue": True,

                "suspend_after_days": 30,

                "invoice_due_days": 7,

                "tax_percentage": 0,

            },

            "integrations": {

                "smtp_host": "",

                "smtp_port": 587,

                "smtp_username": "",

                "smtp_password": "",

                "smtp_use_tls": True,

                "sms_provider": "",

                "sms_api_key": "",

            },

            "branding": {

                "logo_url": "",

                "primary_color": "#1976d2",

                "secondary_color": "#424242",

                "login_page_title": "",

                "login_page_subtitle": "",

                "favicon_url": "",

            },

            "system": {

                "maintenance_mode": False,

                "debug_mode": False,

                "system_timezone": "UTC",

                "audit_log_retention_days": 90,

                "backup_retention_days": 30,

            },

        }

        return defaults.get(

            category,

            {},

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def set_setting(
        db,
        key,
        value,
        *,
        category="general",
        description=None,
        is_editable=True,
    ):

        SettingService._validate_setting_key(
            key,
        )

        setting = (
            SettingService._find_setting(
                db,
                key,
            )
        )

        if setting:

            SettingService._update_setting(

                setting,

                category=category,

                value=value,

                description=description,

                is_editable=is_editable,

            )

        else:

            setting = (
                SettingService
                ._create_setting(

                    db,

                    category=category,

                    key=key,

                    value=value,

                    description=description,

                    is_editable=is_editable,

                )
            )

        db.commit()

        db.refresh(
            setting,
        )

        return setting

    @staticmethod
    def update_category(
        db,
        category,
        values,
    ):

        for key, value in values.items():

            SettingService.set_setting(

                db=db,

                key=key,

                value=value,

                category=category,

            )

        return (
            SettingService.get_category(
                db,
                category,
            )
        )

    @staticmethod
    def enable_setting(
        db,
        key,
        *,
        category="general",
    ):

        return (
            SettingService.set_setting(

                db=db,

                key=key,

                value=True,

                category=category,

            )
        )

    @staticmethod
    def disable_setting(
        db,
        key,
        *,
        category="general",
    ):

        return (
            SettingService.set_setting(

                db=db,

                key=key,

                value=False,

                category=category,

            )
        )
        
    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_value(
        db,
        key,
        default=None,
    ):

        setting = (
            SettingService._find_setting(
                db,
                key,
            )
        )

        if setting is None:

            return default

        return (
            SettingService._cast_value(
                setting.value,
                setting.value_type,
            )
        )

    @staticmethod
    def get_setting(
        db,
        key,
    ):

        return (
            SettingService._find_setting(
                db=db,
                key=key,
                required=True,
            )
        )

    @staticmethod
    def get_boolean(
        db,
        key,
        default=False,
    ):

        value = (
            SettingService.get_value(
                db=db,
                key=key,
                default=default,
            )
        )

        return bool(
            value,
        )

    @staticmethod
    def get_integer(
        db,
        key,
        default=0,
    ):

        value = (
            SettingService.get_value(
                db=db,
                key=key,
                default=default,
            )
        )

        try:

            return int(str(value))

        except (
            TypeError,
            ValueError,
        ):

            return default

    @staticmethod
    def get_string(
        db,
        key,
        default="",
    ):

        value = (
            SettingService.get_value(
                db=db,
                key=key,
                default=default,
            )
        )

        if value is None:

            return default

        return str(
            value,
        )

    @staticmethod
    def get_category(
        db,
        category,
    ):

        settings = (

            db.query(Setting)

            .filter(

                Setting.category == category,

            )

            .order_by(

                Setting.key,

            )

            .all()

        )

        result = (

            SettingService

            ._get_category_defaults(

                category,

            )

            .copy()

        )

        for setting in settings:

            result[
                setting.key
            ] = (
                SettingService._cast_value(
                    setting.value,
                    setting.value_type,
                )
            )

        return result

    @staticmethod
    def get_all_settings(
        db,
    ):

        settings = (

            db.query(Setting)

            .order_by(

                Setting.category,

                Setting.key,

            )

            .all()

        )

        grouped = {}

        for setting in settings:

            grouped.setdefault(

                setting.category,

                {},

            )[

                setting.key

            ] = (

                SettingService._cast_value(

                    setting.value,

                    setting.value_type,

                )

            )

        return grouped