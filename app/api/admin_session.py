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

from app.services.admin_session_service import (
    AdminSessionService,
)

from app.schemas.admin_session import (
    AdminSessionResponse,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.common import (
    JobResultResponse,
)

router = APIRouter(
    prefix="/admin-sessions",
    tags=["Admin Sessions"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.patch(
    "/{admin_session_id}/activity",
    response_model=AdminSessionResponse,
)
def update_activity(
    admin_session_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AdminSessionService.update_activity(
            db=db,
            admin_session_id=admin_session_id,
        )
    )


@router.patch(
    "/{admin_session_id}/close",
    response_model=AdminSessionResponse,
)
def close_session(
    admin_session_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AdminSessionService.close_session(
            db=db,
            admin_session_id=admin_session_id,
        )
    )


@router.patch(
    "/close-all/{admin_user_id}",
    response_model=JobResultResponse,
)
def close_all_sessions(
    admin_user_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    result = (
        AdminSessionService.close_all_sessions(
            db=db,
            admin_user_id=admin_user_id,
        )
    )

    return JobResultResponse(
        processed=result["closed_sessions"],
        message="Admin sessions closed successfully.",
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[AdminSessionResponse],
)
def get_all_sessions(

    admin_user_id: int | None = None,

    is_active: bool | None = None,

    sort_by: str = "login_time",

    sort_order: str = "desc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),
):

    return (
        AdminSessionService.get_all_sessions(

            db=db,

            page=page.page,

            page_size=page.page_size,

            admin_user_id=admin_user_id,

            is_active=is_active,

            sort_by=sort_by,

            sort_order=sort_order,

        )
    )


@router.get(
    "/active",
    response_model=list[AdminSessionResponse],
)
def get_active_sessions(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
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
):

    return (
        AdminSessionService.get_session(
            db=db,
            admin_session_id=admin_session_id,
        )
    )


@router.get(
    "/admin/{admin_user_id}",
    response_model=list[AdminSessionResponse],
)
def get_admin_sessions(
    admin_user_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AdminSessionService.get_admin_sessions(
            db=db,
            admin_user_id=admin_user_id,
        )
    )


@router.get(
    "/admin/{admin_user_id}/active",
    response_model=AdminSessionResponse | None,
)
def get_active_session(
    admin_user_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AdminSessionService.get_active_session(
            db=db,
            admin_user_id=admin_user_id,
        )
    )