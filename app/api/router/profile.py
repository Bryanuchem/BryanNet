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
    RouterProfileResponse,
)

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/router-profiles",

    tags=[
        "Router Profiles",
    ],

)


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}",

    response_model=list[
        RouterProfileResponse
    ],

)

def list_profiles(
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
# Synchronize
# ==========================================================

@router.post(

    "/{router_id}/{plan_id}/synchronize",

)

def synchronize_profile(
    router_id: int,
    plan_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.synchronize_profile(

            db,

            router_id,

            plan_id,

        )

    )