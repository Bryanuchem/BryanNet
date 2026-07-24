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
        "Router IP Pools",
    ],

)


class IPPoolRequest(
    BaseModel,
):

    name: str

    ranges: str

    comment: str | None = None


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}/ip-pools",

)

def list_ip_pools(
    router_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):

    return RouterService.list_ip_pools(
        db,
        router_id,
    )


@router.get(

    "/{router_id}/ip-pools/{pool_id}",

)

def get_ip_pool(
    router_id: int,
    pool_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):

    return RouterService.get_ip_pool(
        db,
        router_id,
        pool_id,
    )


# ==========================================================
# Commands
# ==========================================================

@router.post(

    "/{router_id}/ip-pools",

)

def create_ip_pool(
    router_id: int,
    request: IPPoolRequest,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):

    return RouterService.create_ip_pool(
        db,
        router_id,
        request.name,
        request.ranges,
        request.comment,
    )


@router.put(

    "/{router_id}/ip-pools/{pool_id}",

)

def update_ip_pool(
    router_id: int,
    pool_id: str,
    request: IPPoolRequest,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):

    return RouterService.update_ip_pool(
        db,
        router_id,
        pool_id,
        request.name,
        request.ranges,
        request.comment,
    )


@router.delete(

    "/{router_id}/ip-pools/{pool_id}",

)

def delete_ip_pool(
    router_id: int,
    pool_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):

    return RouterService.delete_ip_pool(
        db,
        router_id,
        pool_id,
    )