from app.providers.router.factory import (
    ProviderFactory,
)


class RouterBootstrapService:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def bootstrap_router(
        db,
        router,
    ):

        provider = (

            ProviderFactory

            .get(

                router,

            )

        )

        provider.ensure_router_bootstrap(
            
            db,

            router,

        )

        return {

            "message": (

                "Router bootstrapped "

                "successfully."

            )

        }
