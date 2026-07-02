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

    return (
        AdminSessionService.close_all_sessions(
            db=db,
            admin_user_id=admin_user_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[AdminSessionResponse],
)
def get_all_sessions(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AdminSessionService.get_all_sessions(
            db,
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