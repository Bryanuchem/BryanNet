from fastapi import HTTPException

from app.models.admin_user import (
    AdminUser,
)

from app.models.role import (
    Role,
)

from app.models.role_permission import (
    RolePermission,
)

from app.models.permission import (
    Permission,
)

from app.schemas.permission import (
    PermissionResponse,
)

from sqlalchemy.orm import (
    joinedload,
)


class PermissionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_permission(
        db,
        permission_id,
    ):

        permission = (

            db.query(
                Permission,
            )

            .filter(
                Permission.permission_id
                == permission_id,
            )

            .first()

        )

        if permission is None:

            raise HTTPException(

                status_code=404,

                detail="Permission not found.",

            )

        return permission

    @staticmethod
    def _find_admin(
        db,
        admin_id,
    ):

        admin = (

            db.query(
                AdminUser,
            )

            .options(

                joinedload(
                    AdminUser.role,
                )

                .joinedload(
                    Role.role_permissions,
                )
                .joinedload(
                    RolePermission.permission,
                ),

            )

            .filter(
                AdminUser.admin_user_id
                == admin_id,
            )

            .first()

        )

        if admin is None:

            raise HTTPException(

                status_code=404,

                detail="Administrator not found.",

            )

        return admin

    @staticmethod
    def _get_permission_set(
        admin,
    ):

        if admin.role is None:

            return set()

        if not admin.role.is_active:

            return set()

        permissions = {

            role_permission
            .permission
            .permission_key

            for role_permission in
            admin.role.role_permissions

            if role_permission.permission

        }

        return permissions

    @staticmethod
    def _build_permission_response(
        permission,
    ):

        return PermissionResponse(

            permission_id=permission.permission_id,

            permission_key=permission.permission_key,

            module=permission.module,

            action=permission.action,

            description=permission.description,

            created_at=permission.created_at,

            updated_at=permission.updated_at,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def is_super_admin(
        admin,
    ):

        return (

            admin.role is not None

            and

            admin.role.role_name
            == "Super Administrator"

        )

    @staticmethod
    def has_permission(
        db,
        admin_id,
        permission_key,
    ):

        admin = (

            PermissionService
            ._find_admin(

                db,

                admin_id,

            )

        )

        if (

            PermissionService
            .is_super_admin(

                admin,

            )

        ):

            return True

        permissions = (

            PermissionService
            ._get_permission_set(

                admin,

            )

        )

        return (

            permission_key
            in permissions

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_admin_permissions(
        db,
        admin_id,
    ):

        admin = (

            PermissionService
            ._find_admin(

                db,

                admin_id,

            )

        )

        if (

            PermissionService
            .is_super_admin(

                admin,

            )

        ):

            return {

                permission.permission_key

                for permission in

                db.query(
                    Permission,
                ).all()

            }

        return (

            PermissionService
            ._get_permission_set(

                admin,

            )

        )

    @staticmethod
    def get_permission(
        db,
        permission_id,
    ):

        permission = (

            PermissionService
            ._find_permission(

                db,

                permission_id,

            )

        )

        return (

            PermissionService
            ._build_permission_response(

                permission,

            )

        )

    @staticmethod
    def get_all_permissions(
        db,
    ):

        permissions = (

            db.query(
                Permission,
            )

            .order_by(

                Permission.module,

                Permission.action,

            )

            .all()

        )

        return [

            PermissionService
            ._build_permission_response(

                permission,

            )

            for permission in permissions

        ]