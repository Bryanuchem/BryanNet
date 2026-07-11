import re

from fastapi import HTTPException

from app.models.role import Role

from app.models.admin_user import (
    AdminUser,
)

from app.models.role_permission import (
    RolePermission,
)

from app.schemas.role import (
    RoleResponse,
)

from sqlalchemy.orm import (
    joinedload,
)


class RoleService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_role(
        db,
        role_id,
        required=False,
    ):

        role = (

            db.query(Role)

            .options(

                joinedload(
                    Role.admin_users,
                ),

                joinedload(
                    Role.role_permissions,
                ),

            )

            .filter(
                Role.role_id == role_id,
            )

            .first()

        )

        if required and role is None:

            raise HTTPException(

                status_code=404,

                detail="Role not found.",

            )

        return role

    @staticmethod
    def _find_role_by_name(
        db,
        role_name,
        required=False,
    ):

        role = (
            db.query(Role)
            .filter(
                Role.role_name == role_name,
            )
            .first()
        )

        if required and role is None:

            raise HTTPException(
                status_code=404,
                detail="Role not found.",
            )

        return role

    @staticmethod
    def _validate_unique_name(
        db,
        role_name,
        exclude_role_id=None,
    ):

        query = (
            db.query(Role)
            .filter(
                Role.role_name == role_name,
            )
        )

        if exclude_role_id is not None:

            query = query.filter(
                Role.role_id != exclude_role_id,
            )

        if query.first():

            raise HTTPException(
                status_code=400,
                detail="Role already exists.",
            )

    @staticmethod
    def _generate_duplicate_name(
        db,
        role_name,
    ):

        base_name = re.sub(

            r" Copy(?: \(\d+\))?$",

            "",

            role_name,

        )

        duplicate_name = (

            f"{base_name} Copy"

        )

        counter = 2

        while (

            db.query(Role)

            .filter(

                Role.role_name == duplicate_name,

            )

            .first()

        ):

            duplicate_name = (

                f"{base_name} Copy ({counter})"

            )

            counter += 1

        return duplicate_name

    @staticmethod
    def _build_role_response(
        role,
    ):

        return RoleResponse(

            role_id=role.role_id,

            role_name=role.role_name,

            description=role.description,

            is_system_role=role.is_system_role,

            is_active=role.is_active,

            assigned_users=len(
                role.admin_users,
            ),

            permission_count=len(
                role.role_permissions,
            ),

            created_at=role.created_at,

            updated_at=role.updated_at,

        )

    @staticmethod
    def _reload_role(
        db,
        role_id,
    ):

        return (

            db.query(Role)

            .options(

                joinedload(
                    Role.admin_users,
                ),

                joinedload(
                    Role.role_permissions,
                ),

            )

            .filter(
                Role.role_id == role_id,
            )

            .first()

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_role(
        db,
        role_name,
        description=None,
        is_system_role=False,
    ):

        RoleService._validate_unique_name(
            db,
            role_name,
        )

        role = Role(

            role_name=role_name,

            description=description,

            is_system_role=is_system_role,

            is_active=True,

        )

        db.add(role)

        db.commit()

        role = RoleService._reload_role(

            db,

            role.role_id,

        )

        return (

            RoleService
            ._build_role_response(

                role,

            )

        )

    @staticmethod
    def update_role(
        db,
        role_id,
        role_name,
        description,
    ):

        role = (
            RoleService._find_role(
                db,
                role_id,
                required=True,
            )
        )

        if role.is_system_role:

            raise HTTPException(
                status_code=400,
                detail="System roles cannot be modified.",
            )

        RoleService._validate_unique_name(
            db,
            role_name,
            role_id,
        )

        role.role_name = role_name

        role.description = description

        db.commit()

        role = RoleService._reload_role(

            db,

            role.role_id,

        )

        return (

            RoleService
            ._build_role_response(

                role,

            )

        )

    @staticmethod
    def activate_role(
        db,
        role_id,
    ):

        role = (
            RoleService._find_role(
                db,
                role_id,
                required=True,
            )
        )

        role.is_active = True

        db.commit()

        role = RoleService._reload_role(

            db,

            role.role_id,

        )

        return (

            RoleService
            ._build_role_response(

                role,

            )

        )

    @staticmethod
    def deactivate_role(
        db,
        role_id,
    ):

        role = (
            RoleService._find_role(
                db,
                role_id,
                required=True,
            )
        )

        if role.is_system_role:

            raise HTTPException(
                status_code=400,
                detail="System roles cannot be deactivated.",
            )

        role.is_active = False

        db.commit()

        role = RoleService._reload_role(

            db,

            role.role_id,

        )

        return (

            RoleService
            ._build_role_response(

                role,

            )

        )

    @staticmethod
    def delete_role(
        db,
        role_id,
    ):

        role = (

            RoleService._find_role(

                db,

                role_id,

                required=True,

            )

        )

        if role.is_system_role:

            raise HTTPException(

                status_code=400,

                detail="System roles cannot be deleted.",

            )

        if role.admin_users:

            raise HTTPException(

                status_code=409,

                detail=(
                    "This role is assigned to one or more administrators."
                ),

            )

        db.delete(

            role,

        )

        db.commit()

        return {

            "message":

                "Role deleted successfully.",

        }


    @staticmethod
    def duplicate_role(
        db,
        role_id,
    ):

        source_role = (

            RoleService._find_role(

                db,

                role_id,

                required=True,

            )

        )

        duplicated_role = Role(

            role_name=RoleService
                ._generate_duplicate_name(

                    db,

                    source_role.role_name,

                ),

            description=source_role.description,

            is_system_role=False,

            is_active=True,

        )

        db.add(

            duplicated_role,

        )

        db.flush()

        for permission in source_role.role_permissions:

            db.add(

                RolePermission(

                    role_id=duplicated_role.role_id,

                    permission_id=permission.permission_id,

                )

            )

        db.commit()

        duplicated_role = (

            RoleService._reload_role(

                db,

                duplicated_role.role_id,

            )

        )

        return (

            RoleService._build_role_response(

                duplicated_role,

            )

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_role(
        db,
        role_id,
    ):

        role = (

            RoleService._find_role(

                db,

                role_id,

                required=True,

            )

        )

        return (

            RoleService._build_role_response(

                role,

            )

        )

    @staticmethod
    def get_role_by_name(
        db,
        role_name,
    ):

        return (
            RoleService._find_role_by_name(
                db,
                role_name,
                required=True,
            )
        )

    @staticmethod
    def get_active_roles(
        db,
    ):

        roles = (

            db.query(Role)

            .options(

                joinedload(
                    Role.admin_users,
                ),

                joinedload(
                    Role.role_permissions,
                ),

            )

            .filter(
                Role.is_active.is_(True),
            )

            .order_by(
                Role.role_name,
            )

            .all()

        )

        return [

            RoleService._build_role_response(
                role,
            )

            for role in roles

        ]

    @staticmethod
    def get_all_roles(
        db,
    ):

        roles = (

            db.query(Role)

            .options(

                joinedload(
                    Role.admin_users,
                ),

                joinedload(
                    Role.role_permissions,
                ),

            )

            .order_by(
                Role.role_name,
            )

            .all()

        )

        return [

            RoleService._build_role_response(
                role,
            )

            for role in roles

        ]
        
       