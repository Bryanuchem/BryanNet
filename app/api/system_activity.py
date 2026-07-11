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

from app.schemas.system_activity import (
    SystemActivityResponse,
)

from app.schemas.pagination import (
    PaginatedResponse,
)

from app.services.system_activity_service import (
    SystemActivityService,
)

router = APIRouter(

    prefix="/system-activity",

    tags=["System Activity"],

)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(

    "/",

    response_model=PaginatedResponse[
        SystemActivityResponse,
    ],

)
def get_system_activity(

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.SYSTEM_ACTIVITY_VIEW,
        ),
    ),

):

    return (

        SystemActivityService.get_all_system_activity(
            db,
        )

    )


@router.get(

    "/{audit_log_id}",

    response_model=SystemActivityResponse,

)
def get_system_activity_record(

    audit_log_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.SYSTEM_ACTIVITY_VIEW,
        ),
    ),

):

    return (

        SystemActivityService.get_system_activity(

            db,

            audit_log_id,

        )

    )