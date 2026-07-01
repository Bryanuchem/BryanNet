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
                Setting.setting_key == key
            )
            .first()
        )

        if required and not setting:

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

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def set_setting(
        db,
        key,
        value,
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

            setting.setting_value = value

        else:

            setting = Setting(
                setting_key=key,
                setting_value=value,
            )

            db.add(setting)

        db.commit()

        db.refresh(setting)

        return setting

    @staticmethod
    def enable_setting(
        db,
        key,
    ):

        return (
            SettingService.set_setting(
                db,
                key,
                "true",
            )
        )

    @staticmethod
    def disable_setting(
        db,
        key,
    ):

        return (
            SettingService.set_setting(
                db,
                key,
                "false",
            )
        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get(
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

        if not setting:

            return default

        return setting.setting_value

    @staticmethod
    def get_setting(
        db,
        key,
    ):

        return (
            SettingService._find_setting(
                db,
                key,
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
            SettingService.get(
                db,
                key,
                str(default).lower(),
            )
        )

        return (
            str(value).lower()
            == "true"
        )

    @staticmethod
    def get_integer(
        db,
        key,
        default=0,
    ):

        value = (
            SettingService.get(
                db,
                key,
                default,
            )
        )

        if value is None:

            return default

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
            SettingService.get(
                db,
                key,
                default,
            )
        )

        return str(value)

    @staticmethod
    def get_all_settings(
        db,
    ):

        return (
            db.query(Setting)
            .order_by(
                Setting.setting_key,
            )
            .all()
        )