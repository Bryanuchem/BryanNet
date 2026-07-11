from typing import cast

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import (
    Session,
)

from app.core.logging import (
    get_logger,
)

from app.database.database import (
    SessionLocal,
)

from app.services.admin_session_service import (
    AdminSessionService,
)

from app.services.admin_user_service import (
    AdminUserService,
)

from app.utils.jwt import (
    verify_access_token,
)


security = HTTPBearer()

logger = get_logger(
    "auth",
)


# ==========================================================
# Database
# ==========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ==========================================================
# Authentication
# ==========================================================

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(
        get_db,
    ),
):

    payload = verify_access_token(
        credentials.credentials,
    )

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    logger.debug(

        "JWT Authentication | sid=%s | sub=%s",

        payload.get(
            "sid",
        ),

        payload.get(
            "sub",
        ),

    )

    admin_user_id = int(
        payload["sub"],
    )

    admin_session_id = int(
        payload["sid"],
    )

    session = (
        AdminSessionService.validate_active_session(
            db=db,
            admin_session_id=admin_session_id,
            admin_user_id=admin_user_id,
        )
    )

    AdminSessionService.touch_active_session(
        session,
    )

    admin = (
        AdminUserService.get_admin(
            db,
            admin_user_id,
        )
    )

    is_active = cast(
        bool,
        admin.is_active,
    )

    if not is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive.",
        )

    db.commit()

    return admin