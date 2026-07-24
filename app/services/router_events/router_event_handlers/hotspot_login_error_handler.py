from sqlalchemy.orm import Session

from app.models.router import Router
from app.schemas.router_event import RouterEventCreate

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.services.router_account_service import (
    RouterAccountService,
)
class HotspotLoginErrorHandler:

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def process(
        db: Session,
        router: Router,
        request: RouterEventCreate,
    ):

        if request.username is None:

            return {

                "success": True,

            }

        username = (

            RouterUsernameService.from_router(

                request.username,

            )

        )

        router_account = (

            RouterAccountService

            .get_username_account(

                db,

                username,

            )

        )

        RouterAccountService.mark_disconnected(

            db,

            router_account.router_account_id,

            message=(

                request.reason

                or

                "Router login failed."

            ),

        )

        return {

            "success": True,

        }