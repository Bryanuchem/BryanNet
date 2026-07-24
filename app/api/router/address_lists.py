from fastapi import (
    APIRouter,
    Depends,
)

from pydantic import (
    BaseModel,
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
        "Router Address Lists",
    ],

)


class AddressListCreate(
    BaseModel,
):

    list_name: str

    address: str

    comment: str | None = None


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}/address-lists",

)

def list_address_lists(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_address_lists(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/address-lists/{address_id}",

)

def get_address_list(
    router_id: int,
    address_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_address_list(

            db,

            router_id,

            address_id,

        )

    )


# ==========================================================
# Commands
# ==========================================================

@router.post(

    "/{router_id}/address-lists",

)

def create_address_list(
    router_id: int,
    request: AddressListCreate,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.create_address_list(

            db,

            router_id,

            request.list_name,

            request.address,

            request.comment,

        )

    )


@router.delete(

    "/{router_id}/address-lists/{address_id}",

)

def delete_address_list(
    router_id: int,
    address_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.delete_address_list(

            db,

            router_id,

            address_id,

        )

    )