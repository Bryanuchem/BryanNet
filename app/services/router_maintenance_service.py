from app.enums import (
    RouterStatus,
)

from app.models.router import (
    Router,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    AUTOMATION_DEVICES,
)

from app.services.notification_service import (
    NotificationService,
)

from app.services.router_service import (
    RouterService,
)


class RouterMaintenanceService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _check_router(
        db,
        router,
    ):

        router = (
            RouterService.refresh_router_status(
                db,
                router.router_id,
            )
        )

        return (
            router.status
            == RouterStatus.ONLINE
        )

    @staticmethod
    def _handle_router_offline(
        db,
        router,
    ):

        #
        # Already offline.
        #
        if (
            router.status
            == RouterStatus.OFFLINE
        ):

            return

        router.status = (
            RouterStatus.OFFLINE
        )

        db.commit()

        db.refresh(
            router,
        )

        NotificationService.send_router_offline(
            router,
        )

    @staticmethod
    def _handle_router_online(
        db,
        router,
    ):

        #
        # Already online.
        #
        if (
            router.status
            == RouterStatus.ONLINE
        ):

            return

        router.status = (
            RouterStatus.ONLINE
        )

        db.commit()

        db.refresh(
            router,
        )

        NotificationService.send_router_online(
            router,
        )
        
    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def run(
        db,
        admin=None,
        session=None,
    ):

        routers = (
            db.query(
                Router,
            )
            .all()
        )

        online = 0

        offline = 0

        checked = 0

        for router in routers:

            is_online = (
                RouterMaintenanceService
                ._check_router(
                    db,
                    router,
                )
            )

            checked += 1

            if is_online:

                RouterMaintenanceService \
                    ._handle_router_online(

                        db,

                        router,

                    )

                online += 1

            else:

                RouterMaintenanceService \
                    ._handle_router_offline(

                        db,

                        router,

                    )

                offline += 1

        result = {

            "processed":
                checked,

            "routers_checked":
                checked,

            "online":
                online,

            "offline":
                offline,

        }

        AuditLogService.log_system_action(

            db=db,

            admin=admin,

            session=session,

            action=AUTOMATION_DEVICES,

            description=(

                "Router maintenance checked "

                f"{result['routers_checked']} router(s): "

                f"{result['online']} online, "

                f"{result['offline']} offline."

            ),

            entity_type="System",

            target_name="Routers",

            new_values=result,

        )

        db.commit()

        return result 