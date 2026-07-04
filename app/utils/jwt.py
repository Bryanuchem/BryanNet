from datetime import (
    datetime,
    timedelta,
    timezone,
)

from typing import Any

from jose import (
    JWTError,
    jwt,
)

from app.core.settings import (
    settings,
)


# ==========================================================
# JWT
# ==========================================================

ISSUER = "BryanNet"


def create_access_token(
    *,
    admin_user_id: int,
    admin_session_id: int,
    role: str,
) -> str:

    now = datetime.now(
        timezone.utc,
    )

    payload = {

        "sub": str(
            admin_user_id,
        ),

        "sid": admin_session_id,

        "role": role,

        "iss": ISSUER,

        "iat": now,

        "exp": (
            now
            + timedelta(
                minutes=settings.jwt_expire_minutes,
            )
        ),

    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def verify_access_token(
    token: str,
) -> dict[str, Any] | None:

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[
                settings.jwt_algorithm,
            ],
        )

        if payload.get(
            "iss",
        ) != ISSUER:

            return None

        if (
            "sub" not in payload
            or "sid" not in payload
            or "role" not in payload
        ):

            return None

        return payload

    except JWTError:

        return None
    