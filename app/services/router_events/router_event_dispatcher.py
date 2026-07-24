from fastapi import (
    HTTPException,
)

from app.enums.router_event_type import (
    RouterEventType,
)

from app.services.router_events.hotspot_login_handler import (
    HotspotLoginHandler,
)

from app.services.router_events.hotspot_logout_handler import (
    HotspotLogoutHandler,
)

from app.services.router_events.router_event_handlers.hotspot_login_error_handler import (
    HotspotLoginErrorHandler,
)

from app.services.router_events.router_event_handlers.router_daily_cleanup_handler import (
    RouterDailyCleanupHandler,
)

class RouterEventDispatcher:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _handlers():

        return {

            RouterEventType.HOTSPOT_LOGIN:
                HotspotLoginHandler.handle,

            RouterEventType.HOTSPOT_LOGOUT:
                HotspotLogoutHandler.handle,

            RouterEventType.HOTSPOT_LOGIN_ERROR:
                HotspotLoginErrorHandler.process,

            RouterEventType.ROUTER_DAILY_CLEANUP:
                RouterDailyCleanupHandler.process,

        }

    # ==========================================================
    # Business Commands
    # ==========================================================
    
    @staticmethod
    def dispatch(
        db,
        payload,
    ):

        handler = (

            RouterEventDispatcher

            ._handlers()

            .get(

                payload.event,

            )

        )

        if handler is None:

            raise HTTPException(

                status_code=400,

                detail=(

                    "Unsupported router "
                    f"event '{payload.event}'."

                ),

            )

        return handler(

            db,

            payload,

        )