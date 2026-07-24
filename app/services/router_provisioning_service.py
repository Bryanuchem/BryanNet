from typing import cast

from app.services.router_account_service import (
    RouterAccount
)

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.router_context_service import (
    RouterContextService,
)

from app.services.router_bootstrap_service import (
    RouterBootstrapService,
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
    def synchronize_active_accounts(
        db,
    ):

        accounts = (

            db.query(

                RouterAccount,

            )

            .filter(

                RouterAccount.is_enabled.is_(

                    True,

                ),

            )

            .order_by(

                RouterAccount.router_account_id,

            )

            .all()

        )

        processed = 0

        successful = 0

        failed = 0

        failures = []

        for account in accounts:

            processed += 1

            try:

                RouterProvisioningService.synchronize_customer_access(

                    db,

                    account.customer_id,

                )

                successful += 1

            except Exception as ex:

                failed += 1

                failures.append(

                    {

                        "customer_id":

                            account.customer_id,

                        "username":

                            account.username,

                        "error":

                            str(

                                ex,

                            ),

                    }

                )

        return {

            "processed": processed,

            "successful": successful,

            "failed": failed,

            "failures": failures,

        }    

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