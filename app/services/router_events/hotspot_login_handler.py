from fastapi import (
    HTTPException,
)

from app.services.device_registration_service import (
    DeviceRegistrationService,
)

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.router_context_service import (
    RouterContextService,
)

from app.services.router_events.session_tracking_service import (
    SessionTrackingService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.services.router_username_service import (
    RouterUsernameService,
)


class HotspotLoginHandler:

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

        context = (

            RouterContextService

            .from_router_account(

                db,

                router_account.router_account_id,

            )

        )

        device = (

            DeviceRegistrationService

            .register_or_touch(

                db=db,

                customer=context.customer,

                mac_address=payload.mac_address,

                device_name=payload.mac_address,

            )

        )

        active_sessions = (

            SessionTrackingService

            .active_sessions(

                db,

                router_account=router_account,

            )

        )

        if (

            active_sessions
            >=
            context.plan.max_devices

        ):

            raise HTTPException(

                status_code=403,

                detail=(

                    "Maximum concurrent "
                    "device limit reached."

                ),

            )

        #
        # RouterOS does NOT create BryanNet sessions.
        #
        # The RouterOS login event can arrive before the
        # browser completes the pending-login callback.
        #
        # If there is no matching BryanNet session yet,
        # treat this as an unmatched confirmation and
        # return success. The callback will create the
        # authoritative session shortly afterwards.
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

        if router_session is None:

            return {

                "success": True,

                "confirmed": False,

                "matched": False,

                "message": (

                    "No matching BryanNet session "
                    "exists yet."

                ),

                "router_account_id": (

                    router_account.router_account_id

                ),

            }

        RouterSessionService.update_runtime(

            db=db,

            router_session=router_session,

            payload=payload,

        )

        RouterAccountService.mark_connected(

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