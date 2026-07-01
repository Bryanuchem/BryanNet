from fastapi import HTTPException

from app.enums import AdminRole


class RoleService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _validate_role(
        role,
    ):

        if role not in AdminRole:

            raise HTTPException(
                status_code=400,
                detail="Invalid administrator role.",
            )

    @staticmethod
    def _can_manage_role(
        current_role,
        target_role,
    ):

        if current_role == AdminRole.SUPER_ADMIN:

            return True

        if (
            target_role
            == AdminRole.SUPER_ADMIN
        ):

            return False

        return True

    # ==========================================================
    # Business Rules
    # ==========================================================

    @staticmethod
    def validate_role_assignment(
        current_role,
        target_role,
    ):

        RoleService._validate_role(
            target_role,
        )

        if not RoleService._can_manage_role(
            current_role,
            target_role,
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "You are not authorized "
                    "to assign this role."
                ),
            )

        return True

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_role(
        role,
    ):

        RoleService._validate_role(
            role,
        )

        return {
            "role": role.value,
            "display_name": (
                role.value
                .replace("_", " ")
                .title()
            ),
        }

    @staticmethod
    def get_roles():

        return [

            {
                "role": role.value,
                "display_name": (
                    role.value
                    .replace("_", " ")
                    .title()
                ),
            }

            for role in AdminRole

        ]