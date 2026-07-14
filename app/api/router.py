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

from app.schemas.router import (
    RouterCreate,
    RouterRead,
    RouterUpdate,
)

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/routers",

    tags=[
        "Routers",
    ],

)


# ==========================================================
# Query
# ==========================================================

@router.get(

    "",

    response_model=list[
        RouterRead,
    ],

)

def get_routers(
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_all_routers(

            db,

        )

    )


@router.get(

    "/{router_id}",

    response_model=RouterRead,

)

def get_router(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_router(

            db,

            router_id,

        )

    )


# ==========================================================
# Commands
# ==========================================================

@router.post(

    "",

    response_model=RouterRead,

)

def create_router(
    request: RouterCreate,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.register_router(

            db,

            request,

        )

    )


@router.put(

    "/{router_id}",

    response_model=RouterRead,

)

def update_router(
    router_id: int,
    request: RouterUpdate,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.update_router(

            db,

            router_id,

            request,

        )

    )


@router.delete(

    "/{router_id}",

)

def delete_router(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.delete_router(

            db,

            router_id,

        )

    )