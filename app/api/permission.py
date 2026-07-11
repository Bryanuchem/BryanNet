from fastapi import (
    APIRouter,
    Depends,
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

from app.schemas.permission import (
    PermissionResponse,
)

from app.services.permission_service import (
    PermissionService,
)

router = APIRouter(

    prefix="/permissions",

    tags=["Permissions"],

)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(

    "/",

    response_model=list[PermissionResponse],

)
def get_permissions(

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.PERMISSIONS_VIEW,
        ),
    ),

):

    return (

        PermissionService
        .get_all_permissions(

            db,

        )

    )


@router.get(

    "/{permission_id}",

    response_model=PermissionResponse,

)
def get_permission(

    permission_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.PERMISSIONS_VIEW
        ),
    ),

):

    return (

        PermissionService
        .get_permission(

            db,

            permission_id,

        )

    )