from app.services.portal_session_service import (
    PortalSessionService,
)

from app.services.router_context_service import (
    RouterContextService,
)

from app.services.router_session_service import (
    RouterSessionService,
)


class SessionTrackingService:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def login(
        db,
        *,
        router_account,
        device,
        payload,
        session_type,
    ):

        router_session = (

            RouterSessionService
            
            .create_session(

                db,

                router_account_id=(
                    router_account.router_account_id
                ),

                router_id=(
                    router_account.router_id
                ),

                username=(
                    router_account.username
                ),

                session_type=session_type,

                ip_address=(
                    payload.ip_address
                ),

                mac_address=(
                    payload.mac_address
                ),

                login_source=(
                    payload.login_by
                ),

                device_id=(

                    device.device_id

                    if device

                    else None

                ),

            )

        )
        
        context = (

            RouterContextService

            .from_router_account(

                db,

                router_account.router_account_id,

            )

        )

        portal_session = (

            PortalSessionService

            .create(

                db,

                customer=(
                    context.customer
                ),

                router=(
                    context.router
                ),

                router_account=(
                    context.router_account
                ),

                router_session=(
                    router_session
                ),

                device=(
                    device
                ),

            )

        )
        
        return {

            "context": context,

            "router_session": router_session,

            "portal_session": portal_session,

        }

    @staticmethod
    def logout(
        db,
        *,
        router_account,
        payload,
    ):

        router_session = (

            RouterSessionService

            .close_session(

                db,

                router_account_id=(
                    router_account.router_account_id
                ),

                mac_address=(
                    payload.mac_address
                ),

                bytes_in=(
                    payload.bytes_in
                ),

                bytes_out=(
                    payload.bytes_out
                ),

                packets_in=(
                    payload.packets_in
                ),

                packets_out=(
                    payload.packets_out
                ),

                disconnect_reason=(
                    payload.disconnect_reason
                ),

            )

        )

        portal_session = (

            PortalSessionService

            .get_active(

                db,

                router_session_id=(
                    router_session.router_session_id
                ),

            )

        )

        if portal_session:

            PortalSessionService.terminate(

                db,

                router_session_id=(

                    router_session.router_session_id

                ),

                termination_reason=(

                    payload.disconnect_reason

                ),

            )

        return router_session

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def active_sessions(
        db,
        *,
        router_account,
    ):

        return (

            RouterSessionService

            .count_active_sessions(

                db,

                router_account_id=(
                    router_account.router_account_id
                ),

            )

        )

    @staticmethod
    def get_active_context(
        db,
        *,
        router_account,
        mac_address=None,
    ):

        router_session = (

            RouterSessionService

            .get_active_session(

                db,

                router_account_id=(
                    router_account.router_account_id
                ),

                mac_address=(
                    mac_address
                ),

            )

        )

        if not router_session:

            return None

        context = (

            RouterContextService

            .from_router_account(

                db,

                router_account.router_account_id,

            )

        )

        portal_session = (

            PortalSessionService

            .get_active(

                db,

                router_session_id=(
                    router_session.router_session_id
                ),

            )

        )

        return {

            "context": context,

            "router_session": router_session,

            "portal_session": portal_session,

        }

    @staticmethod
    def is_online(
        db,
        *,
        router_account,
    ):

        return (

            RouterSessionService

            .is_customer_online(

                db,

                router_account_id=(
                    router_account.router_account_id
                ),

            )

        )