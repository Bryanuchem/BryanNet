from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.services.permission_service import (
    PermissionService,
)

from app.schemas.admin_user import (
    AdminUserActivationRequest,
    AdminUserResponse,
    ChangePasswordRequest,
    ChangeRoleRequest,
    CreateAdminUserRequest,
    UpdateAdminUserRequest,
)

from app.services.admin_user_service import (
    AdminUserService,
)

router = APIRouter(
    prefix="/admin-users",
    tags=["Admin Users"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[AdminUserResponse],
)
def get_admin_users(

    search: str | None = None,

    role_id: int | None = None,

    is_active: bool | None = None,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ADMIN_USERS_VIEW,
        ),
    ),

):

    return (

        AdminUserService.get_all_admins(

            db=db,

            search=search,

            role_id=role_id,

            is_active=is_active,

        )

    )


@router.get(
    "/{admin_user_id}",
    response_model=AdminUserResponse,
)
def get_admin_user(
    admin_user_id: int,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ADMIN_USERS_VIEW,
        ),
    ),
    
):

    return (
        AdminUserService.get_admin(
            db,
            admin_user_id,
        )
    )


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/",
    response_model=AdminUserResponse,
)
def create_admin_user(
    http_request: Request,
    request: CreateAdminUserRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ADMIN_USERS_CREATE,
        ),
    ),

):

    return (
        AdminUserService.create_admin(
            db=db,
            current_admin=admin,
            request=http_request,
            username=request.username,
            email=request.email,
            password=request.password,
            role_id=request.role_id,
        )
    )


@router.put(
    "/{admin_user_id}",
    response_model=AdminUserResponse,
)
def update_admin_user(
    admin_user_id: int,
    http_request: Request,
    request: UpdateAdminUserRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ADMIN_USERS_EDIT,
        ),
    ),

):

    return (
        AdminUserService.update_admin(
            db=db,
            current_admin=admin,
            request=http_request,
            admin_user_id=admin_user_id,
            username=request.username,
            email=request.email,
        )
    )


@router.patch(
    "/{admin_user_id}/password",
    response_model=AdminUserResponse,
)
def change_password(
    admin_user_id: int,
    http_request: Request,
    request: ChangePasswordRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ADMIN_USERS_EDIT,
        ),
    ),
    
):

    return (
        AdminUserService.change_password(
            db=db,
            current_admin=admin,
            request=http_request,
            admin_user_id=admin_user_id,
            password=request.password,
        )
    )


@router.patch(
    "/{admin_user_id}/role",
    response_model=AdminUserResponse,
)
def change_role(
    admin_user_id: int,
    http_request: Request,
    request: ChangeRoleRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ROLES_MANAGE_PERMISSIONS,
        ),
    ),
    
):

    return (
        AdminUserService.change_role(
            db=db,
            current_admin=admin,
            request=http_request,
            admin_user_id=admin_user_id,
            role_id=request.role_id,
        )
    )


@router.patch(
    "/{admin_user_id}/activation",
    response_model=AdminUserResponse,
)
def update_admin_activation(
    admin_user_id: int,
    http_request: Request,
    request: AdminUserActivationRequest,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    required_permission = (

        Permissions.ADMIN_USERS_EDIT

    )

    if not (

        PermissionService
        .has_permission(

            db=db,

            admin_id=admin.admin_user_id,

            permission_key=required_permission,

        )

    ):

        raise HTTPException(

            status_code=403,

            detail="You do not have permission to perform this action.",

        )

    if request.is_active:

        return (
            AdminUserService.activate_admin(
                db=db,
                current_admin=admin,
                request=http_request,
                admin_user_id=admin_user_id,
            )
        )

    return (
        AdminUserService.deactivate_admin(
            db=db,
            current_admin=admin,
            request=http_request,
            admin_user_id=admin_user_id,
        )
    )