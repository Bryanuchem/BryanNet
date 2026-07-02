from fastapi import HTTPException

from app.domain import RouterContext

from app.enums import RouterStatus

from app.models.router import Router

from app.providers.router import (
    ProviderFactory,
)


class RouterService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_router(
        db,
        router_id,
    ):

        router = (
            db.query(Router)
            .filter(
                Router.router_id == router_id
            )
            .first()
        )

        if not router:

            raise HTTPException(
                status_code=404,
                detail="Router not found.",
            )

        return router

    @staticmethod
    def _validate_router(
        router,
    ):

        if router.status == RouterStatus.MAINTENANCE:

            raise HTTPException(
                status_code=400,
                detail="Router is currently in maintenance mode.",
            )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_router(
        db,
        router_data,
    ):

        router = Router(

            router_name=router_data.router_name,

            ip_address=router_data.ip_address,

            api_port=router_data.api_port,

            api_username=router_data.api_username,

            api_password=router_data.api_password,

            location=router_data.location,

            provider=router_data.provider,

            status=RouterStatus.OFFLINE,

        )

        db.add(
            router,
        )

        db.commit()

        db.refresh(
            router,
        )

        return router

    @staticmethod
    def synchronize_customer(
        db,
        context: RouterContext,
    ):

        RouterService._validate_router(
            context.router,
        )

        provider = (
            ProviderFactory.get(
                context.router,
            )
        )

        return (
            provider.synchronize_customer(
                db,
                context,
            )
        )

    @staticmethod
    def disconnect_customer(
        db,
        context: RouterContext,
    ):

        RouterService._validate_router(
            context.router,
        )

        provider = (
            ProviderFactory.get(
                context.router,
            )
        )

        return (
            provider.disconnect_customer(
                db,
                context,
            )
        )

    @staticmethod
    def refresh_router_status(
        db,
        router_id,
    ):

        router = (
            RouterService._find_router(
                db,
                router_id,
            )
        )

        provider = (
            ProviderFactory.get(
                router,
            )
        )

        health = (
            provider.health_check(
                router,
            )
        )

        router.status = (

            RouterStatus.ONLINE

            if health.healthy

            else RouterStatus.OFFLINE

        )

        db.commit()

        db.refresh(
            router,
        )

        return router

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_router(
        db,
        router_id,
    ):

        return (
            RouterService._find_router(
                db,
                router_id,
            )
        )

    @staticmethod
    def get_router_health(
        db,
        router_id,
    ):

        router = (
            RouterService._find_router(
                db,
                router_id,
            )
        )

        provider = (
            ProviderFactory.get(
                router,
            )
        )

        return (
            provider.health_check(
                router,
            )
        )

    @staticmethod
    def get_online_routers(
        db,
    ):

        return (

            db.query(Router)

            .filter(
                Router.status == RouterStatus.ONLINE
            )

            .order_by(
                Router.router_name,
            )

            .all()

        )

    @staticmethod
    def get_all_routers(
        db,
    ):

        return (

            db.query(Router)

            .order_by(
                Router.router_name,
            )

            .all()

        )