from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.session import (
    SessionResponse,
)

from app.services.session_service import (
    SessionService,
)

from app.core.rate_limit import (
    limiter,
)

router = APIRouter(
    prefix="/session",
    tags=["Session"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/telegram/{telegram_user_id}",
    response_model=SessionResponse,
)
@limiter.limit(
    "30/minute",
)
def get_session(
    request: Request,
    telegram_user_id: int,
    first_login: bool = False,
    db: Session = Depends(
        get_db,
    ),
):

    session = (
        SessionService.get_session(
            db=db,
            telegram_user_id=telegram_user_id,
            first_login=first_login,
        )
    )

    return SessionResponse(

        next_action=session["next_action"],

        message=session["message"],

        keyboard=session["keyboard"],

        customer=session["customer"],

    )