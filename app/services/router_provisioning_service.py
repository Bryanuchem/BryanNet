from typing import cast

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.router_context_service import (
    RouterContextService,
)



class RouterProvisioningService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _context(
        db,
        customer_id,
    ):

        router_account = (

            RouterAccountService

            .ensure_router_account(

                db,

                customer_id,

            )

        )

        context = (

            RouterContextService

            .from_router_account(

                db,
                
                cast(
                    
                    int,

                router_account.router_account_id,
                
                ),
            )

        )

        return (

            router_account,

            context,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def ensure_customer_access(
        db,
        customer_id,
    ):

        from app.services.router_service import (
            RouterService,
        )

        router_account, context = (

            RouterProvisioningService

            ._context(

                db,

                customer_id,

            )

        )

        RouterAccountService.activate_account(

            db,

            router_account.router_account_id,

        )

        return (

            RouterService

            .synchronize_customer(

                db,

                context,

            )

        )

    @staticmethod
    def suspend_customer_access(
        db,
        customer_id,
    ):

        from app.services.router_service import (
            RouterService,
        )

        router_account, context = (

            RouterProvisioningService

            ._context(

                db,

                customer_id,

            )

        )

        RouterAccountService.suspend_account(

            db,

            router_account.router_account_id,

        )

        RouterService.disconnect_customer(

            db,

            context,

        )

        return (

            RouterService

            .synchronize_customer(

                db,

                context,

            )

        )

    @staticmethod
    def synchronize_customer_access(
        db,
        customer_id,
    ):

        from app.services.router_service import (
            RouterService,
        )

        _, context = (

            RouterProvisioningService

            ._context(

                db,

                customer_id,

            )

        )

        return (

            RouterService

            .synchronize_customer(

                db,

                context,

            )

        )