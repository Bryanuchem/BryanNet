from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
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

from app.services.auth_service import (
    AuthService,
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
def login(
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

    access_token = (
        create_access_token(
            {

                "sub":
                    str(
                        admin.admin_user_id,
                    ),

                "username":
                    admin.username,

                "role":
                    admin.role.role_name,

            }
        )
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