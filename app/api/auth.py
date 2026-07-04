from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from typing import cast

from sqlalchemy.orm import (
    Session,
)

from app.core.rate_limit import (
    limiter,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.schemas.auth import (
    CurrentAdminResponse,
    LoginRequest,
    LoginResponse,
)

from app.services.admin_session_service import (
    AdminSessionService,
)

from app.services.auth_service import (
    AuthService,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.enums.audit_result import (
    AuditResult,
)

from app.constants.audit_actions import (
    LOGIN,
)

from app.utils.jwt import (
    create_access_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Authentication
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
@limiter.limit(
    "5/minute",
)
def login(
    request: Request,
    credentials: LoginRequest,
    db: Session = Depends(
        get_db,
    ),
):

    admin = (
        AuthService.authenticate(
            db=db,
            username=credentials.username,
            password=credentials.password,
        )
    )

    if admin is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    session = (
        AdminSessionService.create_session(

            db=db,

            admin_user_id=admin.admin_user_id,

            ip_address=(
                request.client.host
                if request.client
                else None
            ),

            user_agent=request.headers.get(
                "user-agent",
            ),

        )
    )

    admin_id = cast(int, admin.admin_user_id)
    admin_session_id = cast(int, session.admin_session_id)

    AuditLogService.log_admin_action(

        db=db,

        admin_id=admin_id,

        admin_session_id=admin_session_id,

        action=LOGIN,

        description=(
            f"Administrator '{admin.username}' logged in."
        ),

        entity_type="AdminUser",

        entity_id=admin_id,

        target_name=str(
            admin.username,
        ),

        result=AuditResult.SUCCESS,

        ip_address=(
            request.client.host
            if request.client
            else None
        ),

        user_agent=request.headers.get(
            "user-agent",
        ),

    )
    
    db.commit()

    access_token = create_access_token(
        admin_user_id=admin_id,
        admin_session_id=admin_session_id,
        role=admin.role.role_name,
    )

    return LoginResponse(
        access_token=access_token,
    )


# ==========================================================
# Current Admin
# ==========================================================

@router.get(
    "/me",
    response_model=CurrentAdminResponse,
)
def get_current_admin_details(
    current_admin=Depends(
        get_current_admin,
    ),
):

    return CurrentAdminResponse(

        admin_user_id=current_admin.admin_user_id,

        username=current_admin.username,

        email=current_admin.email,

        role=current_admin.role.role_name,

        is_active=current_admin.is_active,

    )