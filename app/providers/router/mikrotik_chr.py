import time

from app.domain import (
    RouterContext,
    RouterHealth,
)

from app.providers.router.base import (
    RouterProvider,
)

from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)

from app.providers.router.mikrotik_profile_repository import (
    MikroTikProfileRepository,
)

from app.providers.router.mikrotik_secret_repository import (
    MikroTikSecretRepository,
)

from app.providers.router.mikrotik_session_repository import (
    MikroTikSessionRepository,
)


class MikroTikCHRProvider(
    RouterProvider,
):

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(
        self,
    ):

        self.connection = (
            MikroTikConnection()
        )

        self.profiles = (
            MikroTikProfileRepository()
        )

        self.secrets = (
            MikroTikSecretRepository()
        )

        self.sessions = (
            MikroTikSessionRepository()
        )

    # ==========================================================
    # Customer Synchronization
    # ==========================================================

    def synchronize_customer(
        self,
        db,
        context: RouterContext,
    ):

        api = None

        try:

            api = (

                self.connection

                .connect(

                    context.router,

                )

            )

            profile_name = (

                self.profiles

                .ensure(

                    api,

                    context.plan.plan_id,

                    context.plan.speed_limit_mbps,

                )

            )

            password = (

                context.plaintext_password

            )

            secret = (

                self.secrets

                .ensure(

                    api,

                    username=(
                        context.router_account.username
                    ),

                    password=password,

                    profile=profile_name,

                    enabled=(
                        context.router_account.is_enabled
                    ),

                )

            )

            if (

                context.router_account.is_enabled

            ):

                self.secrets.enable(

                    api,

                    secret,

                )

            else:

                self.secrets.disable(

                    api,

                    secret,

                )

                self.sessions.disconnect_username(

                    api,

                    context.router_account.username,

                )

            return {

                "success": True,

                "message": (

                    "Customer synchronized "

                    "successfully."

                ),

            }

        finally:

            self.connection.disconnect(

                api,

            )
            
    # ==========================================================
    # Customer Connection
    # ==========================================================

    def disconnect_customer(
        self,
        db,
        context: RouterContext,
    ):

        api = None

        try:

            api = (

                self.connection

                .connect(

                    context.router,

                )

            )

            secret = (

                self.secrets

                .find(

                    api,

                    context.router_account.username,

                )

            )

            if secret:

                self.secrets.disable(

                    api,

                    secret,

                )

            self.sessions.disconnect_username(

                api,

                context.router_account.username,

            )

            return {

                "success": True,

                "message": (

                    "Customer disconnected "

                    "successfully."

                ),

            }

        finally:

            self.connection.disconnect(

                api,

            )

    # ==========================================================
    # Router Health
    # ==========================================================

    def health_check(
        self,
        router,
    ):

        start = time.perf_counter()

        api = None

        try:

            api = (

                self.connection

                .connect(

                    router,

                )

            )

            resource = (

                self.connection

                .path(

                    api,

                    "system",

                    "resource",

                )

            )

            system = next(

                iter(

                    resource,

                )

            )

            latency = (

                time.perf_counter()

                - start

            ) * 1000

            return RouterHealth(

                healthy=True,

                connected=True,

                latency_ms=round(

                    latency,

                    2,

                ),

                router_os_version=(

                    system.get(

                        "version",

                    )

                ),

                message=(

                    "Router reachable."

                ),

            )

        except Exception as ex:

            return RouterHealth(

                healthy=False,

                connected=False,

                latency_ms=None,

                router_os_version=None,

                message=str(

                    ex,

                ),

            )

        finally:

            self.connection.disconnect(

                api,

            )