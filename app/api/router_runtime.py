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

from app.schemas.router_runtime import (
    RouterHealthResponse,
    RouterProfileResponse,
    RouterSecretResponse,
    RouterSessionResponse,
)

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/routers",

    tags=[
        "Router Runtime",
    ],

)


# ==========================================================
# Health
# ==========================================================

@router.get(

    "/{router_id}/health",

    response_model=RouterHealthResponse,

)

def health_check(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.health_check(

            db,

            router_id,

        )

    )

# ==========================================================
# Synchronize Router
# ==========================================================

@router.post(

    "/{router_id}/synchronize",

)

def synchronize_router(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.synchronize_router(

            db,

            router_id,

        )

    )

# ==========================================================
# Profiles
# ==========================================================

@router.get(

    "/{router_id}/profiles",

    response_model=list[
        RouterProfileResponse
    ],

)

def get_profiles(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    profiles = (

        RouterService.list_profiles(

            db,

            router_id,

        )

    )

    return [

        RouterProfileResponse(

            id=profile.get(
                ".id",
            ),

            name=profile.get(
                "name",
            ),

            rate_limit=profile.get(
                "rate-limit",
            ),

        )

        for profile in profiles

    ]


# ==========================================================
# Secrets
# ==========================================================

@router.get(

    "/{router_id}/secrets",

    response_model=list[
        RouterSecretResponse
    ],

)

def get_secrets(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    secrets = (

        RouterService.list_secrets(

            db,

            router_id,

        )

    )

    return [

        RouterSecretResponse(

            id=secret.get(
                ".id",
            ),

            username=secret.get(
                "name",
            ),

            profile=secret.get(
                "profile",
            ),

            disabled=(

                secret.get(
                    "disabled",
                )

                in [

                    True,

                    "true",

                    "yes",

                ]

            ),

        )

        for secret in secrets

    ]


# ==========================================================
# Active Sessions
# ==========================================================

@router.get(

    "/{router_id}/sessions",

    response_model=list[
        RouterSessionResponse
    ],

)

def get_sessions(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    sessions = (

        RouterService.list_sessions(

            db,

            router_id,

        )

    )

    return [

        RouterSessionResponse(

            id=session.get(
                ".id",
            ),

            username=session.get(
                "name",
            ),

            address=session.get(
                "address",
            ),

            uptime=session.get(
                "uptime",
            ),

        )

        for session in sessions

    ]