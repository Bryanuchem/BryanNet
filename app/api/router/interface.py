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

    prefix="/routers",

    tags=[
        "Router Interfaces",
    ],

)


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}/interfaces",

)

def list_interfaces(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_interfaces(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/interfaces/{interface_name}",

)

def get_interface(
    router_id: int,
    interface_name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_interface(

            db,

            router_id,

            interface_name,

        )

    )


@router.get(

    "/{router_id}/interfaces/statistics",

)
def list_interface_statistics(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_interface_statistics(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/interfaces/{interface_name}/statistics",

)
def get_interface_statistics(
    router_id: int,
    interface_name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_interface_statistics(

            db,

            router_id,

            interface_name,

        )

    )

# ==========================================================
# Commands
# ==========================================================

@router.post(

    "/{router_id}/interfaces/{interface_name}/enable",

)

def enable_interface(
    router_id: int,
    interface_name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.enable_interface(

            db,

            router_id,

            interface_name,

        )

    )


@router.post(

    "/{router_id}/interfaces/{interface_name}/disable",

)

def disable_interface(
    router_id: int,
    interface_name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.disable_interface(

            db,

            router_id,

            interface_name,

        )

    )