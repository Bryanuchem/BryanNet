from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.auth import (
    LoginRequest,
    LoginResponse
)

from app.services.auth_service import AuthService

from app.utils.jwt import create_access_token

from app.database.dependencies import (
    get_db,
    get_current_admin,
)
from app.schemas.auth import CurrentAdminResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        admin = AuthService.authenticate(
            db=db,
            username=credentials.username,
            password=credentials.password
        )

        if admin is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        print("Creating JWT...")

        access_token = create_access_token(
            {
                "sub": str(admin.admin_user_id),
                "username": admin.username,
                "role": admin.role.value
            }
        )

        print("JWT created successfully")

        return LoginResponse(
            access_token=access_token
        )

    except Exception as e:
        print(f"\nLOGIN ERROR: {type(e).__name__}: {e}")
        raise
    
@router.get(
    "/me",
    response_model=CurrentAdminResponse
)
def me(
    current_admin=Depends(get_current_admin)
):
    return current_admin
