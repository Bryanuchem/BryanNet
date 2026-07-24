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
    RouterHostnameUpdate,
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

@router.patch(

    "/{router_id}/hostname",

    response_model=RouterRead,

)

def update_router_hostname(

    router_id: int,

    request: RouterHostnameUpdate,

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterService.update_hostname(

            db,

            router_id,

            request.hostname,

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
    
# ==========================================================
# Hotspot Desired State
# ==========================================================

@router.post(

    "/{router_id}/hotspot/synchronize",

)

def synchronize_hotspot(

    router_id: int,

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterService.synchronize_hotspot(

            db,

            router_id,

        )

    )


@router.post(

    "/{router_id}/hotspot/verify",

)

def verify_hotspot(

    router_id: int,

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterService.verify_hotspot(

            db,

            router_id,

        )

    )