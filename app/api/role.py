from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
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

from app.schemas.role import (
    CreateRoleRequest,
    DeleteRoleResponse,
    RoleActivationRequest,
    RoleResponse,
    UpdateRoleRequest,
)

from app.services.role_service import (
    RoleService,
)

from app.schemas.permission import (
    RolePermissionResponse,
    UpdateRolePermissionsRequest,
)

from app.services.permission_service import (
    PermissionService,
)

from app.services.role_permission_service import (
    RolePermissionService,
)


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ROLES_VIEW,
        ),
    ),

):

    return (
        RoleService.get_all_roles(
            db,
        )
    )

@router.get(
    "/{role_id}/permissions",
    response_model=list[RolePermissionResponse],
)
def get_role_permissions(

    role_id: int,

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

        RolePermissionService
        .get_role_permissions(

            db,

            role_id,

        )

    )

@router.get(
    "/active",
    response_model=list[RoleResponse],
)
def get_active_roles(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ROLES_VIEW,
        ),
    ),    
    
):

    return (
        RoleService.get_active_roles(
            db,
        )
    )


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: int,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ROLES_VIEW,
        ),
    ),

):

    return (
        RoleService.get_role(
            db,
            role_id,
        )
    )


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/",
    response_model=RoleResponse,
)
def create_role(
    request: CreateRoleRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ROLES_CREATE,
        ),
    ),

):

    return (
        RoleService.create_role(
            db=db,
            role_name=request.role_name,
            description=request.description,
            is_system_role=request.is_system_role,
        )
    )


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
def update_role(
    role_id: int,
    request: UpdateRoleRequest,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.ROLES_EDIT,
        ),
    ),

):

    return (
        RoleService.update_role(
            db=db,
            role_id=role_id,
            role_name=request.role_name,
            description=request.description,
        )
    )

@router.put(
    "/{role_id}/permissions",
    response_model=list[RolePermissionResponse],
)
def update_role_permissions(

    role_id: int,

    request: UpdateRolePermissionsRequest,

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

        RolePermissionService
        .update_role_permissions(

            db,

            role_id,

            request.permission_ids,

        )

    )

@router.patch(
    "/{role_id}/activation",
    response_model=RoleResponse,
)
def update_role_activation(
    role_id: int,
    request: RoleActivationRequest,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    required_permission = (

        Permissions.ROLES_ACTIVATE

        if request.is_active

        else

        Permissions.ROLES_DEACTIVATE

    )

    if not PermissionService.has_permission(

        db=db,

        admin_id=admin.admin_user_id,

        permission_key=required_permission,

    ):

        raise HTTPException(

            status_code=403,

            detail="You do not have permission to perform this action.",

        )

    if request.is_active:

        return (
            RoleService.activate_role(
                db,
                role_id,
            )
        )

    return (
        RoleService.deactivate_role(
            db,
            role_id,
        )
    )

@router.post(
    "/{role_id}/duplicate",
    response_model=RoleResponse,
)
def duplicate_role(

    role_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ROLES_DUPLICATE,
        ),
    ),

):

    return (

        RoleService.duplicate_role(

            db,

            role_id,

        )

    )

@router.delete(
    "/{role_id}",
    response_model=DeleteRoleResponse,
)
def delete_role(

    role_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.ROLES_DELETE,
        ),
    ),

):

    return (

        RoleService.delete_role(

            db,

            role_id,

        )

    )    