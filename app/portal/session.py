from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.portal_session import (
    PortalSessionRegister,
    PortalSessionResponse,
)

from app.services.portal.session_service import (
    PortalSessionService,
)


router = APIRouter(
    prefix="/session",
    tags=["Portal Session"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/register",
    response_model=PortalSessionResponse,
)
def register_session(
    request: PortalSessionRegister,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSessionService.register_session(
            db,
            request,
        )
    )


@router.patch(
    "/{telegram_user_id}",
    response_model=PortalSessionResponse,
)
def refresh_session(
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSessionService.refresh_session(
            db,
            telegram_user_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/{telegram_user_id}",
    response_model=PortalSessionResponse,
)
def get_session(
    telegram_user_id: int,
    first_login: bool = False,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSessionService.get_session(
            db=db,
            telegram_user_id=telegram_user_id,
            first_login=first_login,
        )
    )