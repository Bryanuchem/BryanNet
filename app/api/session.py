from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.session import SessionResponse

from app.services.session_service import SessionService


router = APIRouter(
    prefix="/session",
    tags=["Session"]
)


@router.get(
    "/telegram/{telegram_user_id}",
    response_model=SessionResponse
)
def get_session(
    telegram_user_id: int,
    db: Session = Depends(get_db)
):

    session = SessionService.get_session(
        db=db,
        telegram_user_id=telegram_user_id
    )

    return SessionResponse(
        next_action=session["next_action"],
        message=session["message"],
        keyboard=session["keyboard"],
        customer=session["customer"]
    )