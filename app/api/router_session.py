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
    RouterSessionResponse,
)

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/router-sessions",

    tags=[
        "Router Sessions",
    ],

)


# ==========================================================
# Query
# ==========================================================

@router.get(

    "/{router_id}",

    response_model=list[
        RouterSessionResponse
    ],

)

def list_sessions(
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


# ==========================================================
# Disconnect
# ==========================================================

@router.post(

    "/{router_id}/{username}/disconnect",

)

def disconnect_session(
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

        RouterService.disconnect_session(

            db,

            router_id,

            username,

        )

    )