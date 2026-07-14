from fastapi import HTTPException

from datetime import (
    datetime,
)

from typing import (
    TYPE_CHECKING,
    cast,
)

if TYPE_CHECKING:

    from app.providers.router.mikrotik_chr import (
        MikroTikCHRProvider,
    )

from app.domain import RouterContext

from app.enums import RouterStatus

from app.models.router import Router

from app.providers.router import (
    ProviderFactory,
)

from app.services.router_credential_manager import (
    RouterCredentialManager,
)

from app.services.plan_service import (
    PlanService,
)

from app.services.router_provisioning_service import (
    RouterProvisioningService,
)

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    SYSTEM_CREATED,
    SYSTEM_UPDATED,
)

from app.models.subscription import (
    Subscription,
)

from app.enums import (
    SubscriptionStatus,
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

        encrypted_api_password = (

            RouterCredentialManager
            .encrypt(

                router_data.api_password,

            )

        )
        
        router = Router(

            router_name=router_data.router_name,

            hostname=router_data.hostname,

            location_name=router_data.location_name,

            router_type=router_data.router_type,

            api_port=router_data.api_port,

            api_username=router_data.api_username,

            encrypted_api_password=(
                encrypted_api_password
            ),

            use_ssl=router_data.use_ssl,

            connection_timeout=(
                router_data.connection_timeout
            ),

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

                    "hostname": str(router.hostname),

                    "location_name": str(router.location_name),

                    "router_type": str(router.router_type),

                    "api_port": router.api_port,

                    "api_username": router.api_username,

                    "use_ssl": router.use_ssl,

                    "connection_timeout": (
                        router.connection_timeout
                    ),

                    "status": router.status.value,

                },

            )

        db.commit()

        db.refresh(router)

        return router

    @staticmethod
    def update_router(
        db,
        router_id,
        router_data,
        admin=None,
        session=None,
    ):

        router = (

            RouterService._find_router(

                db,

                router_id,

            )

        )

        old_values = {

            "router_name": str(
                router.router_name,
            ),

            "hostname": str(
                router.hostname,
            ),

            "location_name": str(
                router.location_name,
            ),

            "router_type": str(
                router.router_type,
            ),

            "api_port": router.api_port,

            "api_username": router.api_username,

            "use_ssl": router.use_ssl,

            "connection_timeout": (
                router.connection_timeout
            ),

        }

        router.router_name = (
            router_data.router_name
        )

        router.hostname = (
            router_data.hostname
        )

        router.location_name = (
            router_data.location_name
        )

        router.router_type = (
            router_data.router_type
        )

        router.api_port = (
            router_data.api_port
        )

        router.api_username = (
            router_data.api_username
        )

        if router_data.api_password:

            router.encrypted_api_password = (

                RouterCredentialManager.encrypt(

                    router_data.api_password,

                )

            )

        router.use_ssl = (
            router_data.use_ssl
        )

        router.connection_timeout = (
            router_data.connection_timeout
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

                entity_id=cast(
                    int,
                    router.router_id,
                ),

                target_name=str(
                    router.router_name,
                ),

                result=AuditResult.SUCCESS,

                description=(

                    f"Updated router "

                    f"'{router.router_name}'."

                ),

                old_values=old_values,

                new_values={

                    "router_name": str(
                        router.router_name,
                    ),

                    "hostname": str(
                        router.hostname,
                    ),

                    "location_name": str(
                        router.location_name,
                    ),

                    "router_type": str(
                        router.router_type,
                    ),

                    "api_port": router.api_port,

                    "api_username": router.api_username,

                    "use_ssl": router.use_ssl,

                    "connection_timeout": (
                        router.connection_timeout
                    ),

                },

            )

        db.commit()

        db.refresh(

            router,

        )

        return router

    @staticmethod
    def delete_router(
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

        if router.router_accounts:

            raise HTTPException(

                status_code=400,

                detail=(

                    "Cannot delete a router that "

                    "still has router accounts."

                ),

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

                entity_id=cast(
                    int,
                    router.router_id,
                ),

                target_name=str(
                    router.router_name,
                ),

                result=AuditResult.SUCCESS,

                description=(

                    f"Deleted router "

                    f"'{router.router_name}'."

                ),

                old_values={

                    "router_name": str(
                        router.router_name,
                    ),

                    "hostname": str(
                        router.hostname,
                    ),

                    "location_name": str(
                        router.location_name,
                    ),

                    "router_type": str(
                        router.router_type,
                    ),

                },

            )

        db.delete(

            router,

        )

        db.commit()

        return {

            "success": True,

            "message":

                "Router deleted successfully.",

        }

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
    def disconnect_session(
        db,
        router_id,
        username,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            disconnected = (

                provider.sessions.disconnect_username(

                    api,

                    username,

                )

            )

            return {

                "success": disconnected,

                "message": (

                    "Session disconnected."

                    if disconnected

                    else "No active session found."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

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

        router.last_health_check = (

            datetime.now()

        )

        router.last_latency_ms = (

            health.latency_ms

        )

        router.router_os_version = (

            health.router_os_version

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

    @staticmethod
    def synchronize_router(
        db,
        router_id,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )
        # ======================================================
        # Synchronize Profiles
        # ======================================================

        plans = (

            PlanService.get_active_plans(

                db,

            )

        )
        

        plan_ids = [

            plan.plan_id

            for plan in plans

        ]

        profiles_processed = 0

        profiles_failed = 0

        profile_failures = []

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            for plan in plans:

                try:

                    provider.profiles.ensure(

                        api,

                        plan.plan_id,

                        plan.speed_limit_mbps,

                    )

                    profiles_processed += 1

                except Exception as ex:

                    profiles_failed += 1

                    profile_failures.append(

                        {

                            "plan_id": (

                                plan.plan_id

                            ),

                            "plan_name": (

                                plan.plan_name

                            ),

                            "error": str(

                                ex,

                            ),

                        }

                    )

        finally:

            orphan_profiles_removed = (

                provider.profiles.delete_orphans(

                    api,

                    plan_ids,

                )

            )

            provider.connection.disconnect(

                api,

            )

        # ======================================================
        # Synchronize Customers
        # ======================================================

        active_subscriptions = (

            db.query(

                Subscription,

            )

            .filter(

                Subscription.plan_id.in_(
                    
                    plan_ids,
                ),

                Subscription.status

                == SubscriptionStatus.ACTIVE,

            )

            .all()

        )

        customers_processed = 0

        customers_failed = 0

        customer_failures = []

        for subscription in active_subscriptions:

            try:

                RouterProvisioningService.synchronize_customer_access(

                    db,

                    subscription.customer_id,

                )

                customers_processed += 1

            except Exception as ex:

                customers_failed += 1

                customer_failures.append(

                    {

                        "customer_id": (

                            subscription.customer_id

                        ),

                        "subscription_id": (

                            subscription.subscription_id

                        ),

                        "error": str(

                            ex,

                        ),

                    }

                )
                
        return {

            "success": (

                profiles_failed == 0

                and

                customers_failed == 0

            ),

            "router": (

                router.router_name

            ),

            "profiles": {

                "processed": (

                    profiles_processed

                ),

                "failed": (

                    profiles_failed

                ),

                "removed": (

                    orphan_profiles_removed

                ),

                "failures": (

                    profile_failures

                ),

            },

            "customers": {

                "processed": (

                    customers_processed

                ),

                "failed": (

                    customers_failed

                ),

                "failures": (

                    customer_failures

                ),

            },

            "message": (

                f"Synchronized "

                f"{profiles_processed} profile(s) "

                f"and "

                f"{customers_processed} customer(s)."

            ),

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
        
    @staticmethod
    def health_check(
        db,
        router_id,
    ):

        router = (

            RouterService.get_router(

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
    def list_profiles(
        db,
        router_id,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            return (

                provider.profiles.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def synchronize_profile(
        db,
        router_id,
        plan_id,
    ):

        from app.services.plan_service import (
            PlanService,
        )

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        plan = (

            PlanService.get_plan(

                db,

                plan_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            profile = (

                provider.profiles.ensure(

                    api,

                    plan.plan_id,

                    plan.speed_limit_mbps,

                )

            )

            return {

                "success": True,

                "profile": profile,

                "message":

                    "Profile synchronized successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def list_secrets(
        db,
        router_id,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )
        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            return (

                provider.secrets.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def enable_secret(
        db,
        router_id,
        username,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            provider.secrets.enable(

                api,

                username,

            )

            return {

                "success": True,

                "message":

                    "Secret enabled successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def delete_secret(
        db,
        router_id,
        username,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            provider.secrets.delete(

                api,

                username,

            )

            return {

                "success": True,

                "message":

                    "Secret deleted successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def disable_secret(
        db,
        router_id,
        username,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            provider.secrets.disable(

                api,

                username,

            )

            return {

                "success": True,

                "message":
                    "Secret disabled successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def list_sessions(
        db,
        router_id,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        provider = cast(

            "MikroTikCHRProvider",

            ProviderFactory.get(

                router,

            ),

        )

        api = None

        try:

            api = (

                provider.connection.connect(

                    router,

                )

            )

            return (

                provider.sessions.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )
