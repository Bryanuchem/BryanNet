from fastapi import (
    HTTPException,
)

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.services.session_lifecycle_service import (
    SessionLifecycleService,
)


class HotspotLogoutHandler:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def handle(
        db,
        payload,
    ):

        username = (

            RouterUsernameService

            .from_router(

                payload.username,

            )

        )

        router_account = (

            RouterAccountService

            .get_username_account(

                db,

                username,

            )

        )

        #
        # RouterOS logout is a confirmation event.
        #
        # Find the BryanNet session that was already
        # created by the login lifecycle.
        #

        router_session = (

            RouterSessionService

            .get_active_session(

                db,

                router_account_id=(

                    router_account.router_account_id

                ),

                mac_address=(

                    payload.mac_address

                ),

            )

        )

        #
        # Logout may arrive after BryanNet has already
        # expired or disconnected the session.
        #
        # Treat it as an unmatched confirmation.
        #

        if router_session is None:

            return {

                "success": True,

                "confirmed": False,

                "matched": False,

                "message": (

                    "No matching BryanNet session "
                    "exists."

                ),

                "router_account_id": (

                    router_account.router_account_id

                ),

            }

        #
        # Persist RouterOS runtime information before
        # terminating the BryanNet lifecycle.
        #

        RouterSessionService.update_runtime(

            db=db,

            router_session=router_session,

            payload=payload,

        )

        SessionLifecycleService.terminate_session(

            db,

            router_session=router_session,

            reason="router_logout",

        )

        RouterAccountService.mark_disconnected(

            db,

            router_account.router_account_id,

        )

        return {

            "success": True,

            "confirmed": True,

            "matched": True,

            "router_session_id": (

                router_session.router_session_id

            ),

            "router_account_id": (

                router_account.router_account_id

            ),

        }