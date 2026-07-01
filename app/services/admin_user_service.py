from fastapi import HTTPException

from passlib.context import CryptContext

from app.enums import AdminRole

from app.models.admin_user import AdminUser


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class AdminUserService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_admin(
        db,
        admin_user_id,
    ):

        admin = (
            db.query(AdminUser)
            .filter(
                AdminUser.admin_user_id == admin_user_id
            )
            .first()
        )

        if not admin:

            raise HTTPException(
                status_code=404,
                detail="Administrator not found.",
            )

        return admin

    @staticmethod
    def _validate_username(
        db,
        username,
        exclude_admin_id=None,
    ):

        query = (
            db.query(AdminUser)
            .filter(
                AdminUser.username == username
            )
        )

        if exclude_admin_id is not None:

            query = query.filter(
                AdminUser.admin_user_id
                != exclude_admin_id
            )

        if query.first():

            raise HTTPException(
                status_code=400,
                detail="Username already exists.",
            )

    @staticmethod
    def _validate_email(
        db,
        email,
        exclude_admin_id=None,
    ):

        query = (
            db.query(AdminUser)
            .filter(
                AdminUser.email == email
            )
        )

        if exclude_admin_id is not None:

            query = query.filter(
                AdminUser.admin_user_id
                != exclude_admin_id
            )

        if query.first():

            raise HTTPException(
                status_code=400,
                detail="Email already exists.",
            )

    @staticmethod
    def _validate_super_admin(
        db,
        admin,
    ):

        if admin.role != AdminRole.SUPER_ADMIN:

            return

        total_super_admins = (
            db.query(AdminUser)
            .filter(
                AdminUser.role == AdminRole.SUPER_ADMIN,
                AdminUser.is_active.is_(True),
            )
            .count()
        )

        if total_super_admins <= 1:

            raise HTTPException(
                status_code=400,
                detail=(
                    "At least one active "
                    "Super Admin must remain."
                ),
            )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_admin(
        db,
        username,
        email,
        password,
        role=AdminRole.ADMIN,
    ):

        AdminUserService._validate_username(
            db,
            username,
        )

        AdminUserService._validate_email(
            db,
            email,
        )

        admin = AdminUser(

            username=username,

            email=email,

            password_hash=pwd_context.hash(
                password,
            ),

            role=role,

            is_active=True,

        )

        db.add(admin)

        db.commit()

        db.refresh(admin)

        return admin

    @staticmethod
    def update_admin_details(
        db,
        admin_user_id,
        username,
        email,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

        AdminUserService._validate_username(
            db,
            username,
            admin_user_id,
        )

        AdminUserService._validate_email(
            db,
            email,
            admin_user_id,
        )

        admin.username = username
        admin.email = email

        db.commit()

        db.refresh(admin)

        return admin

    @staticmethod
    def change_password(
        db,
        admin_user_id,
        password,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

        admin.password_hash = (
            pwd_context.hash(
                password,
            )
        )

        db.commit()

        db.refresh(admin)

        return admin

    @staticmethod
    def change_role(
        db,
        current_admin,
        admin_user_id,
        role,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

        if (
            current_admin.admin_user_id
            == admin.admin_user_id
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "You cannot change "
                    "your own role."
                ),
            )

        from app.services.role_service import (
            RoleService,
        )

        RoleService.validate_role_assignment(
            current_role=current_admin.role,
            target_role=role,
        )

        admin.role = role

        db.commit()

        db.refresh(admin)

        return admin

    @staticmethod
    def activate_admin(
        db,
        admin_user_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

        admin.is_active = True

        db.commit()

        db.refresh(admin)

        return admin

    @staticmethod
    def deactivate_admin(
        db,
        admin_user_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

        AdminUserService._validate_super_admin(
            db,
            admin,
        )

        admin.is_active = False

        db.commit()

        db.refresh(admin)

        return admin

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_admin(
        db,
        admin_user_id,
    ):

        return (
            AdminUserService._find_admin(
                db,
                admin_user_id,
            )
        )

    @staticmethod
    def get_active_admins(
        db,
    ):

        return (
            db.query(AdminUser)
            .filter(
                AdminUser.is_active.is_(True)
            )
            .order_by(
                AdminUser.username,
            )
            .all()
        )

    @staticmethod
    def get_all_admins(
        db,
    ):

        return (
            db.query(AdminUser)
            .order_by(
                AdminUser.username,
            )
            .all()
        )