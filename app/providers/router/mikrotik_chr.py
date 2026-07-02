import routeros_api

from fastapi import HTTPException

from app.domain import (
    RouterContext,
    RouterHealth,
)

from app.providers.router.base import (
    RouterProvider,
)


class MikroTikCHRProvider(
    RouterProvider,
):

    # ==========================================================
    # Connection Helpers
    # ==========================================================

    def _connect(
        self,
        router,
    ):

        try:

            api_pool = (
                routeros_api.RouterOsApiPool(

                    host=router.ip_address,

                    username=router.api_username,

                    password=router.api_password,

                    port=router.api_port,

                    plaintext_login=True,

                )
            )

            api = (
                api_pool.get_api()
            )

            return (
                api_pool,
                api,
            )

        except Exception as ex:

            raise HTTPException(
                status_code=503,
                detail=(
                    f"Unable to connect to router: {ex}"
                ),
            )

    def _disconnect(
        self,
        api_pool,
    ):

        if api_pool:

            api_pool.disconnect()

    def _execute(
        self,
        api,
        resource,
    ):

        try:

            return api.get_resource(
                resource,
            )

        except Exception as ex:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"RouterOS resource error: {ex}"
                ),
            )
            
    # ==========================================================
    # PPP Secret Helpers
    # ==========================================================

    def _find_secret(
        self,
        api,
        username,
    ):

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        secrets = (
            secret_resource.get(
                name=username,
            )
        )

        if not secrets:

            return None

        return secrets[0]

    def _create_secret(
        self,
        api,
        context: RouterContext,
    ):

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        profile = (
            self._find_or_create_profile(
                api,
                context,
            )
        )

        secret_resource.add(

            name=(
                context.router_account.username
            ),

            password=(
                context.router_account.password
            ),

            profile=profile,

            disabled=(
                "no"
                if context.router_account.is_enabled
                else "yes"
            ),

            comment=(
                f"BryanNet Customer "
                f"{context.customer.customer_id}"
            ),

        )

    def _update_secret(
        self,
        api,
        context: RouterContext,
    ):

        secret = (
            self._find_secret(
                api,
                context.router_account.username,
            )
        )

        if not secret:

            self._create_secret(
                api,
                context,
            )

            return

        profile = (
            self._find_or_create_profile(
                api,
                context,
            )
        )

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        secret_resource.set(

            id=secret[".id"],

            password=(
                context.router_account.password
            ),

            profile=profile,

            disabled=(
                "no"
                if context.router_account.is_enabled
                else "yes"
            ),

            comment=(
                f"BryanNet Customer "
                f"{context.customer.customer_id}"
            ),

        )

    def _enable_secret(
        self,
        api,
        username,
    ):

        secret = (
            self._find_secret(
                api,
                username,
            )
        )

        if not secret:

            return

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        secret_resource.set(

            id=secret[".id"],

            disabled="no",

        )

    def _disable_secret(
        self,
        api,
        username,
    ):

        secret = (
            self._find_secret(
                api,
                username,
            )
        )

        if not secret:

            return

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        secret_resource.set(

            id=secret[".id"],

            disabled="yes",

        )

    def _delete_secret(
        self,
        api,
        username,
    ):

        secret = (
            self._find_secret(
                api,
                username,
            )
        )

        if not secret:

            return

        secret_resource = (
            self._execute(
                api,
                "/ppp/secret",
            )
        )

        secret_resource.remove(
            id=secret[".id"],
        )            
        
    # ==========================================================
    # PPP Profile Helpers
    # ==========================================================

    def _find_profile(
        self,
        api,
        profile_name,
    ):

        profile_resource = (
            self._execute(
                api,
                "/ppp/profile",
            )
        )

        profiles = (
            profile_resource.get(
                name=profile_name,
            )
        )

        if not profiles:

            return None

        return profiles[0]

    def _create_profile(
        self,
        api,
        context: RouterContext,
    ):

        profile_resource = (
            self._execute(
                api,
                "/ppp/profile",
            )
        )

        profile_resource.add(

            name=(
                context.plan.plan_name
            ),

            rate_limit=(
                f"{context.plan.speed_limit_mbps}M/"
                f"{context.plan.speed_limit_mbps}M"
            ),

        )

        return (
            context.plan.plan_name
        )

    def _update_profile(
        self,
        api,
        context: RouterContext,
    ):

        profile = (
            self._find_profile(
                api,
                context.plan.plan_name,
            )
        )

        if not profile:

            return (
                self._create_profile(
                    api,
                    context,
                )
            )

        profile_resource = (
            self._execute(
                api,
                "/ppp/profile",
            )
        )

        profile_resource.set(

            id=profile[".id"],

            rate_limit=(
                f"{context.plan.speed_limit_mbps}M/"
                f"{context.plan.speed_limit_mbps}M"
            ),

        )

        return (
            context.plan.plan_name
        )

    def _find_or_create_profile(
        self,
        api,
        context: RouterContext,
    ):

        profile = (
            self._find_profile(
                api,
                context.plan.plan_name,
            )
        )

        if profile:

            self._update_profile(
                api,
                context,
            )

            return (
                context.plan.plan_name
            )

        return (
            self._create_profile(
                api,
                context,
            )
        )

    # ==========================================================
    # RouterProvider Implementation
    # ==========================================================

    def synchronize_customer(
        self,
        db,
        context: RouterContext,
    ):

        api_pool = None

        try:

            api_pool, api = (
                self._connect(
                    context.router,
                )
            )

            self._update_secret(
                api,
                context,
            )

            if context.router_account.is_enabled:

                self._enable_secret(
                    api,
                    context.router_account.username,
                )

            else:

                self._disable_secret(
                    api,
                    context.router_account.username,
                )

            return {

                "success": True,

                "message":
                    "Customer synchronized successfully.",

            }

        finally:

            self._disconnect(
                api_pool,
            )

    def disconnect_customer(
        self,
        db,
        context: RouterContext,
    ):

        api_pool = None

        try:

            api_pool, api = (
                self._connect(
                    context.router,
                )
            )

            self._disable_secret(
                api,
                context.router_account.username,
            )

            return {

                "success": True,

                "message":
                    "Customer disconnected successfully.",

            }

        finally:

            self._disconnect(
                api_pool,
            )

    # ==========================================================
    # Health Check
    # ==========================================================

    def health_check(
        self,
        router,
    ):

        api_pool = None

        try:

            api_pool, api = (
                self._connect(
                    router,
                )
            )

            self._execute(
                api,
                "/system/resource",
            )

            return RouterHealth(

                healthy=True,

                connected=True,

                latency_ms=None,

                router_os_version=None,

                message=(
                    "Router connection successful."
                ),

            )

        except Exception as ex:

            return RouterHealth(

                healthy=False,

                connected=False,

                latency_ms=None,

                router_os_version=None,

                message=str(ex),

            )

        finally:

            self._disconnect(
                api_pool,
            )        