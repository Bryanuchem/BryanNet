from app.models.permission import (
    Permission,
)

from app.models.role import (
    Role,
)

from app.models.role_permission import (
    RolePermission,
)

from app.schemas.permission import (
    RolePermissionResponse,
)


class RolePermissionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _build_role_permission_response(
        role_permission,
    ):

        permission = (
            role_permission.permission
        )

        return RolePermissionResponse(

            role_id=role_permission.role_id,

            permission_id=permission.permission_id,

            permission_key=permission.permission_key,

            module=permission.module,

            action=permission.action,

            description=permission.description,

        )

    @staticmethod
    def _find_role(
        db,
        role_id,
    ):

        role = (

            db.query(
                Role,
            )

            .filter(
                Role.role_id
                == role_id,
            )

            .first()

        )

        if role is None:

            from fastapi import HTTPException

            raise HTTPException(

                status_code=404,

                detail="Role not found.",

            )

        return role

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

            from fastapi import HTTPException

            raise HTTPException(

                status_code=404,

                detail=(
                    f"Permission "
                    f"{permission_id} "
                    f"not found."
                ),

            )

        return permission

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_role_permissions(
        db,
        role_id,
    ):

        role_permissions = (

            db.query(
                RolePermission,
            )

            .join(
                Permission,
            )

            .filter(
                RolePermission.role_id
                == role_id,
            )

            .order_by(

                Permission.module,

                Permission.action,

            )

            .all()

        )

        return [

            RolePermissionService
            ._build_role_permission_response(

                role_permission,

            )

            for role_permission in role_permissions

        ]

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def update_role_permissions(

        db,

        role_id,

        permission_ids,

    ):

        role = (

            RolePermissionService
            ._find_role(

                db,

                role_id,

            )

        )

        permissions = [

            RolePermissionService
            ._find_permission(

                db,

                permission_id,

            )

            for permission_id
            in permission_ids

        ]

        db.query(
            RolePermission,
        ).filter(
            RolePermission.role_id
            == role_id,
        ).delete()

        for permission in permissions:

            db.add(

                RolePermission(

                    role_id=role.role_id,

                    permission_id=permission.permission_id,

                )

            )

        db.commit()

        return (

            RolePermissionService
            .get_role_permissions(

                db,

                role_id,

            )

        )