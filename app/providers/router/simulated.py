from datetime import datetime, UTC

from app.providers.router.base import (
    RouterProvider,
)

from app.domain import (
    RouterContext,
    RouterHealth,
)

from app.services.virtual_router_account_service import (
    VirtualRouterAccountService,
)


class SimulatedRouterProvider(
    RouterProvider,
):

    # ==========================================================
    # Private Helpers
    # ==========================================================

    def _validate_context(
        self,
        context: RouterContext,
    ):

        if context.customer is None:

            raise ValueError(
                "RouterContext.customer cannot be None."
            )

        if context.subscription is None:

            raise ValueError(
                "RouterContext.subscription cannot be None."
            )

        if context.plan is None:

            raise ValueError(
                "RouterContext.plan cannot be None."
            )

        if context.router is None:

            raise ValueError(
                "RouterContext.router cannot be None."
            )

        if context.router_account is None:

            raise ValueError(
                "RouterContext.router_account cannot be None."
            )

        if context.devices is None:

            raise ValueError(
                "RouterContext.devices cannot be None."
            )

    def _reconcile_virtual_router(
        self,
        db,
        context: RouterContext,
    ):

        return (

            VirtualRouterAccountService
            .synchronize_virtual_account(

                db,

                context,

            )

        )

    def _finalize_sync(
        self,
        virtual_account,
    ):

        virtual_account.last_synchronized_at = (
            datetime.now(UTC)
        )

        return virtual_account

    # ==========================================================
    # Customer Synchronization
    # ==========================================================

    def synchronize_customer(
        self,
        db,
        context: RouterContext,
    ):

        self._validate_context(
            context,
        )

        virtual_account = (

            self._reconcile_virtual_router(

                db,

                context,

            )

        )

        virtual_account = (

            self._finalize_sync(

                virtual_account,

            )

        )

        db.commit()

        db.refresh(
            virtual_account,
        )

        return virtual_account
    
    # ==========================================================
    # Customer Connection
    # ==========================================================

    def disconnect_customer(
        self,
        db,
        context: RouterContext,
    ):

        self._validate_context(
            context,
        )

        virtual_account = (

            VirtualRouterAccountService
            .set_connection_status(

                db,

                context.router_account.router_account_id,

                False,

            )

        )

        return virtual_account

    # ==========================================================
    # Router Health
    # ==========================================================

    def health_check(
        self,
        router,
    ):

        return RouterHealth(

            healthy=True,

            connected=True,

            latency_ms=1.0,

            router_os_version="Virtual Router",

            message=(
                "Virtual router provider is operational."
            ),

        )    