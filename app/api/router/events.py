"""  
from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.router_event import (
    RouterEventCreate,
)

from app.services.router_event_service import (
    RouterEventService,
)

router = APIRouter(

    prefix="/router-events",

    tags=[
        "Router Events",
    ],

)


# ==========================================================
# Router Events
# ==========================================================
  
@router.post(

    "",

)

def receive_router_event(

    request: RouterEventCreate,

    db: Session = Depends(

        get_db,

    ),

):

    return (

        RouterEventService

        .process(

            db,

            request,

        )

    )
    
"""    

from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.router_event import (
    RouterEventCreate,
)

from app.services.router_event_service import (
    RouterEventService,
)

router = APIRouter(

    prefix="/router-events",

    tags=[
        "Router Events",
    ],

)


@router.post("")
async def receive_router_event(

    request: Request,

    db: Session = Depends(
        get_db,
    ),

):

    body = await request.body()

    print("=" * 80)
    print(repr(body))
    print("=" * 80)

    payload = RouterEventCreate.model_validate_json(
        body,
    )

    return (

        RouterEventService

        .process(

            db,

            payload,

        )

    )