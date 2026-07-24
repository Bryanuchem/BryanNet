from sqlalchemy.orm import Session

from app.models.router import Router
from app.schemas.router_event import RouterEventCreate

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.router_events.session_tracking_service import (
    SessionTrackingService,
)
class HotspotLogoutHandler:

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

        SessionTrackingService.logout(

            db,

            router_account=router_account,

            payload=request,

        )

        RouterAccountService.mark_disconnected(

            db,

            router_account.router_account_id,

        )

        return {

            "success": True,

        }