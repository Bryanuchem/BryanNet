from fastapi import HTTPException

from sqlalchemy.orm import (
    joinedload,
)

from app.utils.security import (
    hash_password,
)

from app.models.admin_user import (
    AdminUser,
)

from app.schemas.admin_user import (
    AdminUserResponse,
)

from app.services.role_service import (
    RoleService,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.enums.audit_result import (
    AuditResult,
)

from app.models.role import Role

from app.models.role_permission import RolePermission

from app.models.permission import Permission

from app.constants.audit_actions import (
    CREATE_ADMIN,
    UPDATE_ADMIN,
    CHANGE_ROLE,
    ACTIVATE_ADMIN,
    DEACTIVATE_ADMIN,
    RESET_ADMIN_PASSWORD,
)

class AdminUserService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_admin(
        db,
        admin_user_id,
        required=False,
    ):

        admin = (
            db.query(AdminUser)
            
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
                AdminUser.admin_user_id == admin_user_id,
            )
            .first()
        )

        if required and admin is None:

            raise HTTPException(
                status_code=404,
                detail="Administrator not found.",
            )

        return admin

    @staticmethod
    def _save(
        db,
        admin,
    ):

        db.add(admin)

        db.commit()

        db.refresh(admin)

        admin = (

            AdminUserService._find_admin(

                db,

                admin.admin_user_id,

                required=True,

            )

        )

        return (

            AdminUserService._build_admin_response(

                admin,

            )

        )


# ==========================================================
# Response Mappers
# ==========================================================

    @staticmethod
    def _build_admin_response(
        admin,
    ):

        permissions = sorted(

            [

                rp.permission.permission_key

                for rp in admin.role.role_permissions

            ]

        )

        return AdminUserResponse(

            admin_user_id=admin.admin_user_id,

            username=admin.username,

            email=admin.email,

            role_id=admin.role_id,

            role_name=admin.role.role_name,
            
            permissions=permissions,

            is_active=admin.is_active,

            created_at=admin.created_at,

            updated_at=admin.updated_at,

        )
    

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_admin(
        db,
        current_admin,
        request,
        username,
        email,
        password,
        role_id,
    ):

        if (
            db.query(AdminUser)
            .filter(
                AdminUser.username == username,
            )
            .first()
        ):

            raise HTTPException(
                status_code=400,
                detail="Username already exists.",
            )

        if (
            db.query(AdminUser)
            .filter(
                AdminUser.email == email,
            )
            .first()
        ):

            raise HTTPException(
                status_code=400,
                detail="Email already exists.",
            )

        RoleService.get_role(
            db,
            role_id,
        )

        admin = AdminUser(

            username=username,

            email=email,

            password_hash=hash_password(
                password,
            ),

            role_id=role_id,

            is_active=True,

        )

        response = (

            AdminUserService._save(

                db,

                admin,

            )

        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=CREATE_ADMIN,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"created administrator "

                f"'{response.username}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            new_values={

                "username": response.username,

                "email": response.email,

                "role": response.role_name,

            },

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(

                "user-agent",

            ),

        )

        db.commit()

        return response
        
    @staticmethod
    def update_admin(
        db,
        current_admin,
        request,
        admin_user_id,
        username,
        email,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        old_values = {

            "username": admin.username,

            "email": admin.email,

        }

        if (
            db.query(AdminUser)
            .filter(
                AdminUser.username == username,
                AdminUser.admin_user_id != admin_user_id,
            )
            .first()
        ):

            raise HTTPException(
                status_code=400,
                detail="Username already exists.",
            )

        if (
            db.query(AdminUser)
            .filter(
                AdminUser.email == email,
                AdminUser.admin_user_id != admin_user_id,
            )
            .first()
        ):

            raise HTTPException(
                status_code=400,
                detail="Email already exists.",
            )

        admin.username = username

        admin.email = email

        response = (
            AdminUserService._save(
                db,
                admin,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=UPDATE_ADMIN,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"updated administrator "

                f"'{response.username}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            old_values=old_values,

            new_values={

                "username": response.username,

                "email": response.email,

            },

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )

        db.commit()

        return response

    @staticmethod
    def change_password(
        db,
        current_admin,
        request,
        admin_user_id,
        password,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        admin.password_hash = hash_password(
            password,
        )

        response = (
            AdminUserService._save(
                db,
                admin,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=RESET_ADMIN_PASSWORD,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"reset the password for "

                f"administrator "

                f"'{response.username}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )

        db.commit()

        return response

    @staticmethod
    def change_role(
        db,
        current_admin,
        request,
        admin_user_id,
        role_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        RoleService.get_role(
            db,
            role_id,
        )

        old_role = admin.role.role_name

        admin.role_id = role_id

        response = (
            AdminUserService._save(
                db,
                admin,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=CHANGE_ROLE,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"changed role of "

                f"'{response.username}' "

                f"from '{old_role}' "

                f"to '{response.role_name}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            old_values={

                "role": old_role,

            },

            new_values={

                "role": response.role_name,

            },

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )

        db.commit()

        return response

    @staticmethod
    def activate_admin(
        db,
        current_admin,
        request,
        admin_user_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        admin.is_active = True

        response = (
            AdminUserService._save(
                db,
                admin,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=ACTIVATE_ADMIN,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"activated administrator "

                f"'{response.username}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            old_values={

                "is_active": False,

            },

            new_values={

                "is_active": True,

            },

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )

        db.commit()

        return response

    @staticmethod
    def deactivate_admin(
        db,
        current_admin,
        request,
        admin_user_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        admin.is_active = False

        response = (
            AdminUserService._save(
                db,
                admin,
            )
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=current_admin.admin_user_id,

            action=DEACTIVATE_ADMIN,

            description=(

                f"Administrator "

                f"'{current_admin.username}' "

                f"deactivated administrator "

                f"'{response.username}'."

            ),

            entity_type="AdminUser",

            entity_id=response.admin_user_id,

            target_name=response.username,

            result=AuditResult.SUCCESS,

            old_values={

                "is_active": True,

            },

            new_values={

                "is_active": False,

            },

            ip_address=(

                request.client.host

                if request.client

                else None

            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )

        db.commit()

        return response

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_admin(
        db,
        admin_user_id,
    ):

        admin = (
            AdminUserService._find_admin(
                db,
                admin_user_id,
                required=True,
            )
        )

        return (
            AdminUserService._build_admin_response(
                admin,
            )
        )

    @staticmethod
    def get_active_admins(
        db,
    ):

        return (
            db.query(AdminUser)
            .options(
                joinedload(
                    AdminUser.role,
                )
            )
            .filter(
                AdminUser.is_active.is_(True),
            )
            .order_by(
                AdminUser.username,
            )
            .all()
        )

    @staticmethod
    def get_all_admins(

        db,

        search=None,

        role_id=None,

        is_active=None,

    ):

        query = (

            db.query(
                AdminUser,
            )

            .options(

                joinedload(
                    AdminUser.role,
                ),

            )

        )

        if search:

            query = query.filter(

                (AdminUser.username.ilike(f"%{search}%"))

                |

                (AdminUser.email.ilike(f"%{search}%"))

            )

        if role_id is not None:

            query = query.filter(

                AdminUser.role_id == role_id,

            )

        if is_active is not None:

            query = query.filter(

                AdminUser.is_active == is_active,

            )

        admins = (

            query

            .order_by(
                AdminUser.username,
            )

            .all()

        )

        return [

            AdminUserService
            ._build_admin_response(
                admin,
            )

            for admin in admins

        ]