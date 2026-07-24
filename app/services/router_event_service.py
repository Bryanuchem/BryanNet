from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.router import Router
from app.schemas.router_event import RouterEventCreate
from app.services.router_events.router_event_dispatcher import (
    RouterEventDispatcher,
)


class RouterEventService:

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def process(
        db: Session,
        request: RouterEventCreate,
    ):

        router = (

            db.query(
                Router,
            )

            .filter(

                Router.router_identifier
                == request.router_identifier,

                Router.router_secret
                == request.router_secret,

            )

            .first()

        )

        if not router:

            raise HTTPException(

                status_code=401,

                detail=(
                    "Invalid router credentials."
                ),

            )

        return (

            RouterEventDispatcher

            .dispatch(

                db=db,

                payload=request,

            )

        )