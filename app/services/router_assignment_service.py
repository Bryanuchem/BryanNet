from fastapi import HTTPException

from app.enums import (
    RouterProviderType,
    RouterStatus,
)

from app.models.router import Router
from app.models.router_account import RouterAccount


class RouterAssignmentService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_online_routers(
        db,
    ):

        return (

            db.query(

                Router,

            )

            .filter(

                Router.status == RouterStatus.ONLINE,

            )

            .order_by(

                Router.router_id,

            )

            .all()

        )

    @staticmethod
    def select_router(
        db,
    ):

        routers = (

            RouterAssignmentService

            ._get_online_routers(

                db,

            )

        )

        if not routers:

            raise HTTPException(

                status_code=503,

                detail=(

                    "No online routers are available."

                ),

            )

        for router in routers:

            if (

                router.router_type

                == RouterProviderType.MIKROTIK_CHR

            ):

                return router

        for router in routers:

            if (

                router.router_type

                == RouterProviderType.MIKROTIK_PHYSICAL

            ):

                return router

        return routers[0]

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_assigned_router(
        db,
        customer_id,
    ):

        account = (

            db.query(
                RouterAccount,
            )

            .filter(
                RouterAccount.customer_id == customer_id,
            )

            .first()

        )

        if not account:

            return None

        return (

            db.query(
                Router,
            )

            .filter(
                Router.router_id == account.router_id,
            )

            .first()

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def assign_router(
        db,
        customer_id,
    ):

        #
        # Already assigned.
        #

        router = (

            RouterAssignmentService
            .get_assigned_router(

                db,

                customer_id,

            )

        )

        if router:

            return router

        #
        # Version 1 strategy.
        #

        return (

            RouterAssignmentService

            .select_router(

                db,

            )

        )