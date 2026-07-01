from fastapi import HTTPException

from app.enums import RouterStatus

from app.models.router import Router


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

    @staticmethod
    def _get_provider(
        router,
    ):
        """
        Placeholder.

        Later this will return the appropriate
        Router Provider implementation.

        Simulator

        MikroTik CHR

        Physical MikroTik
        """

        return None

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
            status=RouterStatus.OFFLINE,
        )

        db.add(router)

        db.commit()

        db.refresh(router)

        return router

    @staticmethod
    def test_connection(
        db,
        router_id,
    ):

        router = (
            RouterService._find_router(
                db,
                router_id,
            )
        )

        RouterService._validate_router(
            router,
        )

        provider = (
            RouterService._get_provider(
                router,
            )
        )

        #
        # Future:
        #
        # return provider.test_connection()
        #

        return {
            "connected": True,
            "message": "Connection successful.",
        }

    @staticmethod
    def synchronize_router(
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
            RouterService._get_provider(
                router,
            )
        )

        #
        # Future:
        #
        # provider.synchronize()
        #

        return {
            "message": "Router synchronized.",
        }

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
            RouterService._get_provider(
                router,
            )
        )

        #
        # Future:
        #
        # router.status =
        # provider.get_status()
        #

        db.commit()

        db.refresh(router)

        return router

    @staticmethod
    def disconnect_router(
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
            RouterService._get_provider(
                router,
            )
        )

        #
        # Future:
        #
        # provider.disconnect()
        #

        return {
            "message": "Router disconnected.",
        }

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

        return {
            "router_id": router.router_id,
            "router_name": router.router_name,
            "status": router.status,
        }

    @staticmethod
    def get_router_statistics(
        db,
        router_id,
    ):

        router = (
            RouterService._find_router(
                db,
                router_id,
            )
        )

        return {
            "router_id": router.router_id,
            "router_name": router.router_name,
        }

    @staticmethod
    def get_online_routers(
        db,
    ):

        return (
            db.query(Router)
            .filter(
                Router.status == RouterStatus.ONLINE
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
                Router.router_name
            )
            .all()
        )