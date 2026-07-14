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

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/router-secrets",

    tags=[
        "Router Secrets",
    ],

)


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}",

)

def list_router_secrets(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_secrets(

            db,

            router_id,

        )

    )


# ==========================================================
# Enable
# ==========================================================

@router.post(

    "/{router_id}/{username}/enable",

)

def enable_secret(
    router_id: int,
    username: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.enable_secret(

            db,

            router_id,

            username,

        )

    )


# ==========================================================
# Disable
# ==========================================================

@router.post(

    "/{router_id}/{username}/disable",

)

def disable_secret(
    router_id: int,
    username: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.disable_secret(

            db,

            router_id,

            username,

        )

    )


# ==========================================================
# Delete
# ==========================================================

@router.delete(

    "/{router_id}/{username}",

)

def delete_secret(
    router_id: int,
    username: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.delete_secret(

            db,

            router_id,

            username,

        )

    )