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

from app.schemas.admin_session import (
    AdminSessionResponse,
)

from app.services.admin_session_service import (
    AdminSessionService,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
)

router = APIRouter(
    prefix="/sessions",
    tags=["Login Sessions"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        AdminSessionResponse,
    ],
)
def get_sessions(

    search: str | None = None,

    is_active: bool | None = None,

    device: str | None = None,

    browser: str | None = None,

    sort_by: str = "login_time",

    sort_order: str = "desc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.LOGIN_SESSIONS_VIEW,
        ),
    ),

):

    return (

        AdminSessionService.get_all_sessions(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

            is_active=is_active,

            device=device,

            browser=browser,

            sort_by=sort_by,

            sort_order=sort_order,

        )

    )


@router.get(
    "/active",
    response_model=list[
        AdminSessionResponse,
    ],
)
def get_active_sessions(

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.LOGIN_SESSIONS_VIEW,
        ),
    ),

):

    return (
        AdminSessionService.get_active_sessions(
            db,
        )
    )


@router.get(
    "/{admin_session_id}",
    response_model=AdminSessionResponse,
)
def get_session(

    admin_session_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.LOGIN_SESSIONS_VIEW,
        ),
    ),

):

    return (
        AdminSessionService.get_session(
            db,
            admin_session_id,
        )
    )


@router.get(
    "/admin/{admin_user_id}",
    response_model=list[
        AdminSessionResponse,
    ],
)
def get_admin_sessions(

    admin_user_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.LOGIN_SESSIONS_VIEW,
        ),
    ),

):

    return (
        AdminSessionService.get_admin_sessions(
            db,
            admin_user_id,
        )
    )


# ==========================================================
# Business Commands
# ==========================================================

@router.patch(
    "/{admin_session_id}/revoke",
    response_model=AdminSessionResponse,
)
def revoke_session(

    admin_session_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.LOGIN_SESSIONS_REVOKE,
        ),
    ),

):

    return (
        AdminSessionService.close_session(
            db,
            admin_session_id,
        )
    )