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
        "Router Queues",
    ],

)

# ==========================================================
# Simple Queues
# ==========================================================

@router.get(

    "/{router_id}/queues/simple",

)

def list_simple_queues(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_simple_queues(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/queues/simple/{queue_id}",

)

def get_simple_queue(
    router_id: int,
    queue_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_simple_queue(

            db,

            router_id,

            queue_id,

        )

    )


# ==========================================================
# Queue Trees
# ==========================================================

@router.get(

    "/{router_id}/queues/tree",

)

def list_queue_trees(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_queue_trees(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/queues/tree/{queue_id}",

)

def get_queue_tree(
    router_id: int,
    queue_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_queue_tree(

            db,

            router_id,

            queue_id,

        )

    )