from typing import cast

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from sqlalchemy.orm import (
    Session,
    joinedload,
)

from app.database.database import SessionLocal
from app.models.admin_user import AdminUser
from app.utils.jwt import verify_access_token


security = HTTPBearer()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    payload = verify_access_token(
        credentials.credentials,
    )

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    admin = (
        db.query(AdminUser)
        .options(
            joinedload(AdminUser.role)
        )
        .filter(
            AdminUser.admin_user_id == int(payload["sub"])
        )
        .first()
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found.",
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

    return admin