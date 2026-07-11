from typing import (
    Any,
    cast,
)

from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.utils.security import (
    verify_password,
)

from app.models.admin_user import (
    AdminUser,
)


class AuthService:

    @staticmethod
    def authenticate(
        db: Session,
        username: str,
        password: str,
    ):

        admin = (

            db.query(AdminUser)

            .filter(
                AdminUser.username == username,
            )

            .first()

        )

        if (
            admin is None
            or not verify_password(
                password,
                str(admin.password_hash),
            )
        ):

            return None

        return admin

    @staticmethod
    def get_current_admin(
        db: Session,
        admin_user_id: int,
    ):

        admin = (

            db.query(AdminUser)

            .options(

                joinedload(
                    AdminUser.role,
                )

                .joinedload(
                    cast(Any,"role_permissions"),
                )

                .joinedload(
                    cast(Any,"permission"),
                ),

            )

            .filter(

                AdminUser.admin_user_id
                == admin_user_id,

            )

            .first()

        )

        if admin is None:

            return None

        permissions = sorted({

            role_permission.permission.permission_name

            for role_permission in
            admin.role.role_permissions

        })

        return {

            "admin_user_id":
                admin.admin_user_id,

            "username":
                admin.username,

            "email":
                admin.email,

            "role":
                admin.role.role_name,

            "permissions":
                permissions,

            "is_active":
                admin.is_active,

        }