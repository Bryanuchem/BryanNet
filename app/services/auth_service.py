from typing import cast

from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser
from app.utils.security import verify_password


class AuthService:

    @staticmethod
    def authenticate(
        db: Session,
        username: str,
        password: str
    ) -> AdminUser | None:

        admin = (
            db.query(AdminUser)
            .filter(
                AdminUser.username == username
            )
            .first()
        )

        if admin is None:
            return None

        hashed_password = cast(
            str,
            admin.password_hash
        )

        if not verify_password(
            password,
            hashed_password
        ):
            return None

        if not admin.is_active:
            return None

        return admin