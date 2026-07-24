from app.models.router import (
    Router,
)

from app.models.router_account import (
    RouterAccount,
)

from app.services.router_provisioning_service import (
    RouterProvisioningService,
)

from app.services.router_service import (
    RouterService,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    SYSTEM_UPDATED,
)

from app.enums.audit_result import (
    AuditResult,
)


class RouterOperationsService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _log_migration(
        db,
        customer_id,
        username,
        old_router_id,
        new_router_id,
    ):

        AuditLogService.log_system_action(

            db=db,

            action=SYSTEM_UPDATED,

            entity_type="RouterAccount",

            entity_id=customer_id,

            target_name=username,

            result=AuditResult.SUCCESS,

            description=(

                f"Repaired router assignment "

                f"from router "

                f"{old_router_id} "

                f"to "

                f"{new_router_id}."

            ),

            old_values={

                "router_id": old_router_id,

            },

            new_values={

                "router_id": new_router_id,

            },

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def repair_assignments(
        db,
    ):

        online_routers = (

            RouterService.get_online_routers(

                db,

            )

        )

        if not online_routers:

            return {

                "processed": 0,

                "migrated": 0,

                "skipped": 0,

                "failed": 1,

                "failures": [

                    "No online routers available.",

                ],

            }

        target_router = (

            online_routers[0]

        )

        accounts = (

            db.query(

                RouterAccount,

            )

            .order_by(

                RouterAccount.router_account_id,

            )

            .all()

        )

        processed = 0

        migrated = 0

        skipped = 0

        failed = 0

        failures = []

        for account in accounts:

            processed += 1

            try:

                router = (

                    db.query(

                        Router,

                    )

                    .filter(

                        Router.router_id
                        == account.router_id,

                    )

                    .first()

                )

                if (

                    router

                    and

                    router.router_type.name
                    != "SIMULATED"

                ):

                    skipped += 1

                    continue

                old_router_id = (

                    account.router_id

                )

                account.router_id = (

                    target_router.router_id

                )

                db.commit()

                db.refresh(

                    account,

                )

                RouterProvisioningService.synchronize_customer_access(

                    db,

                    account.customer_id,

                )

                RouterOperationsService._log_migration(

                    db,

                    account.customer_id,

                    account.username,

                    old_router_id,

                    target_router.router_id,

                )

                migrated += 1

            except Exception as ex:

                db.rollback()

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

            "migrated": migrated,

            "skipped": skipped,

            "failed": failed,

            "failures": failures,

        }

    @staticmethod
    def rebalance(
        db,
    ):

        return (

            RouterOperationsService

            .repair_assignments(

                db,

            )

        )
        
    @staticmethod
    def migrate_customer(
        db,
        customer_id,
        target_router_id,
    ):

        account = (

            db.query(

                RouterAccount,

            )

            .filter(

                RouterAccount.customer_id
                == customer_id,

            )

            .first()

        )

        if account is None:

            raise ValueError(

                "Router account not found."

            )

        target_router = (

            db.query(

                Router,

            )

            .filter(

                Router.router_id
                == target_router_id,

            )

            .first()

        )

        if target_router is None:

            raise ValueError(

                "Target router not found."

            )

        old_router_id = (

            account.router_id

        )

        account.router_id = (

            target_router.router_id

        )

        db.commit()

        db.refresh(

            account,

        )

        RouterProvisioningService.synchronize_customer_access(

            db,

            customer_id,

        )

        RouterOperationsService._log_migration(

            db,

            customer_id,

            account.username,

            old_router_id,

            target_router.router_id,

        )

        return {

            "customer_id": customer_id,

            "old_router_id": old_router_id,

            "new_router_id": target_router.router_id,

        }
        
    @staticmethod
    def migrate_router(
        db,
        source_router_id,
        target_router_id,
    ):

        accounts = (

            db.query(

                RouterAccount,

            )

            .filter(

                RouterAccount.router_id
                == source_router_id,

            )

            .all()

        )

        processed = 0

        migrated = 0

        failed = 0

        failures = []

        for account in accounts:

            processed += 1

            try:

                RouterOperationsService.migrate_customer(

                    db,

                    account.customer_id,

                    target_router_id,

                )

                migrated += 1

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

            "migrated": migrated,

            "failed": failed,

            "failures": failures,

        }