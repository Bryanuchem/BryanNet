from fastapi import HTTPException

from app.domain import RouterContext

from app.enums import RouterStatus

from app.models.router import Router

from app.providers.router import (
    ProviderFactory,
)

from typing import cast

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    SYSTEM_CREATED,
    SYSTEM_UPDATED,
)

from app.enums.audit_result import AuditResult


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
        admin=None,
        session=None,
    ):

        router = Router(

            router_name=router_data.router_name,

            management_ip=router_data.management_ip,

            location_name=router_data.location_name,

            router_type=router_data.router_type,

            status=RouterStatus.OFFLINE,

        )

        db.add(router)

        db.flush()

        if admin:

            AuditLogService.log_admin_action(

                db=db,

            admin_id=cast(
                int,
                admin.admin_user_id,
            ),

            admin_session_id=(
                cast(
                    int,
                    session.admin_session_id,
                )
                if session
                else None
            ),

                action=SYSTEM_CREATED,

                entity_type="Router",

                entity_id=cast(int, router.router_id),

                target_name=str(router.router_name),

                result=AuditResult.SUCCESS,

                description=(
                    f"Registered router '{router.router_name}'."
                ),

                new_values={

                    "management_ip": str(router.management_ip),

                    "location_name": str(router.location_name),

                    "router_type": str(router.router_type),

                    "status": router.status.value,

                },

            )

        db.commit()

        db.refresh(router)

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
        admin=None,
        session=None,
    ):

        router = (
            RouterService._find_router(
                db,
                router_id,
            )
        )

        old_status = router.status

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

        if admin:

            AuditLogService.log_admin_action(

                db=db,

                admin_id=cast(
                    int,
                    admin.admin_user_id,
                ),

                admin_session_id=(
                    cast(
                        int,
                        session.admin_session_id,
                    )
                    if session
                    else None
                ),

                action=SYSTEM_UPDATED,

                entity_type="Router",

                entity_id=cast(int, router.router_id),

                target_name=str(router.router_name),

                result=AuditResult.SUCCESS,

                description=(
                    f"Refreshed router '{router.router_name}' status."
                ),

                old_values={
                    "status": old_status.value,
                },

                new_values={
                    "status": router.status.value,
                },

            )

        db.commit()

        db.refresh(router)

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
        page=1,
        page_size=25,
    ):

        return (

            db.query(Router)

            .order_by(
                Router.router_name,
            )

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )