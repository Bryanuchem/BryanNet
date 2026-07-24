from fastapi import (
    APIRouter,
    Depends,
    Query,
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
        "Router Logs",
    ],

)


@router.get(

    "/{router_id}/logs",

)

def list_logs(
    router_id: int,
    topic: str | None = Query(
        default=None,
    ),
    severity: str | None = Query(
        default=None,
    ),
    date: str | None = Query(
        default=None,
    ),
    search: str | None = Query(
        default=None,
    ),
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    if topic or severity or date or search:

        return (

            RouterService.filter_logs(

                db,

                router_id,

                topic=topic,

                severity=severity,

                date=date,

                search=search,

            )

        )

    return (

        RouterService.list_logs(

            db,

            router_id,

        )

    )