from fastapi import HTTPException

import secrets

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

from sqlalchemy.orm import Session

from app.services.router_bootstrap_service import (
    RouterBootstrapService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.models.router_account import (
    RouterAccount,
)

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    SYSTEM_CREATED,
    SYSTEM_UPDATED,
)

from app.services.router_context_service import (
    RouterContextService,
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

    @staticmethod
    def _list_firewall_rules(
        db,
        router_id,
        method_name,
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

            return getattr(

                provider.firewall,

                method_name,

            )(

                api,

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _get_firewall_rule(
        db,
        router_id,
        method_name,
        rule_id,
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

            return getattr(

                provider.firewall,

                method_name,

            )(

                api,

                rule_id,

            )

        finally:

            provider.connection.disconnect(

                api,

            )          

    @staticmethod
    def _list_queues(
        db,
        router_id,
        method_name,
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

            return getattr(

                provider.queues,

                method_name,

            )(

                api,

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _get_queue(
        db,
        router_id,
        method_name,
        queue_id,
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

            return getattr(

                provider.queues,

                method_name,

            )(

                api,

                queue_id,

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _list_dhcp(
        db,
        router_id,
        method_name,
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

            return getattr(

                provider.dhcp,

                method_name,

            )(

                api,

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _get_dhcp(
        db,
        router_id,
        method_name,
        object_id,
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

            return getattr(

                provider.dhcp,

                method_name,

            )(

                api,

                object_id,

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def _list_dhcp_leases(
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

                provider.dhcp_leases.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _get_dhcp_lease(
        db,
        router_id,
        lease_id,
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

                provider.dhcp_leases.get(

                    api,

                    lease_id,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    # ==========================================================
    # Hotspot
    # ==========================================================

    @staticmethod
    def _hotspot(
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

                provider.hotspot

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def _list_hotspot(
        db,
        router_id,
        method,
    ):

        hotspot = (

            RouterService._hotspot(

                db,

                router_id,

            )

        )

        return getattr(

            hotspot,

            method,

        )()


    @staticmethod
    def _get_hotspot(
        db,
        router_id,
        method,
        item_id,
    ):

        hotspot = (

            RouterService._hotspot(

                db,

                router_id,

            )

        )

        return getattr(

            hotspot,

            method,

        )(

            item_id,

        )

    # ==========================================================
    # Backup
    # ==========================================================

    @staticmethod
    def _backup(
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

                provider.backups

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    @staticmethod
    def _list_backup(
        db,
        router_id,
        method,
    ):

        backup = (

            RouterService._backup(

                db,

                router_id,

            )

        )

        return getattr(

            backup,

            method,

        )()

    @staticmethod
    def _get_backup(
        db,
        router_id,
        method,
        item_id,
    ):

        backup = (

            RouterService._backup(

                db,

                router_id,

            )

        )

        return getattr(

            backup,

            method,

        )(

            item_id,

        )

    @staticmethod
    def _execute_backup(
        db,
        router_id,
        method,
        *args,
    ):

        backup = (

            RouterService._backup(

                db,

                router_id,

            )

        )

        return getattr(

            backup,

            method,

        )(

            *args,

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

            router_secret=secrets.token_urlsafe(
                48,
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

    # ==========================================================
    # Update Router Hostname
    # ==========================================================

    @staticmethod
    def update_hostname(
        db,
        router_id,
        hostname,
    ):

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

        )

        router.hostname = hostname

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

        from app.services.router_bootstrap_service import (
            RouterBootstrapService,
        )

        RouterBootstrapService.bootstrap_router(

            db,

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
    def enable_interface(
        db,
        router_id,
        interface_name,
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

            interface = (

                provider.interfaces.get(

                    api,

                    interface_name,

                )

            )

            provider.interfaces.enable(

                api,

                interface,

            )

            return {

                "success": True,

                "message":

                    "Interface enabled successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def disable_interface(
        db,
        router_id,
        interface_name,
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

            interface = (

                provider.interfaces.get(

                    api,

                    interface_name,

                )

            )

            provider.interfaces.disable(

                api,

                interface,

            )

            return {

                "success": True,

                "message":

                    "Interface disabled successfully.",

            }

        finally:

            provider.connection.disconnect(

                api,

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

        RouterService.health_check(

            db,

            router_id,

        )

        router = (

            RouterService.get_router(

                db,

                router_id,

            )

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

                    f"Refreshed router "

                    f"'{router.router_name}' status."

                ),

                new_values={

                    "status": (

                        router.status.value

                    ),

                    "latency_ms": (

                        router.last_latency_ms

                    ),

                    "router_os_version": (

                        router.router_os_version

                    ),

                    "last_health_check": str(

                        router.last_health_check,

                    ),

                },

            )

        return router

    @staticmethod
    def synchronize_router(
        db: Session,
        router_id: int,
    ):

        router = RouterService._find_router(
            db,
            router_id,
        )

        bootstrap = (
            RouterBootstrapService.bootstrap_router(
                db,
                router,
            )
        )

        hotspot = (
            RouterService.synchronize_hotspot(
                db,
                router_id,
            )
        )

        customer_summary = {

            "processed": 0,

            "failed": 0,

            "failures": [],

        }

        accounts = (

            db.query(
                RouterAccount,
            )

            .filter(

                RouterAccount.router_id
                == router.router_id,

            )

            .all()

        )

        for account in accounts:

            try:

                context = RouterContextService.from_router_account(
                    db,
                    account,
                )

                RouterService.synchronize_customer(
                    db,
                    context,
                )

                customer_summary[
                    "processed"
                ] += 1

            except Exception as exc:

                customer_summary[
                    "failed"
                ] += 1

                customer_summary[
                    "failures"
                ].append(

                    {

                        "customer_id": (
                            account.customer_id
                        ),

                        "username": (
                            account.username
                        ),

                        "error": str(
                            exc,
                        ),

                    }

                )

        provider = ProviderFactory.get(
            router,
        )

        connection = provider.connection.connect(
            router,
        )

        try:

            hotspot_sessions = (

                provider.hotspot.get_active(
                    connection,
                )

            )

            ppp_sessions = (

                provider.sessions.get_all(
                    connection,
                )

            )

        finally:

            provider.connection.disconnect(
                connection,
            )

        runtime = (

            RouterSessionService

            .synchronize_runtime(

                db,

                router_id=router.router_id,

                hotspot_sessions=hotspot_sessions,

                ppp_sessions=ppp_sessions,

            )

        )

        return {

            "success": True,

            "router": router.router_name,

            "bootstrap": bootstrap,

            "hotspot": hotspot,

            "customers": customer_summary,

            "runtime": runtime,

            "message": (
                "Router synchronized successfully."
            ),

        }
        
    # ==========================================================
    # Hotspot Desired State
    # ==========================================================

    @staticmethod
    def synchronize_hotspot(
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

                provider.synchronize_hotspot(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def verify_hotspot(
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

                provider.verify_hotspot(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def authenticate_router(
        db,
        router_identifier,
        router_secret,
    ):

        router = (

            db.query(
                Router,
            )

            .filter(

                Router.router_identifier
                == router_identifier,

            )

            .first()

        )

        if (

            not router

            or

            router.router_secret
            != router_secret

        ):

            raise HTTPException(

                status_code=401,

                detail="Invalid router credentials.",

            )

        return router

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

        db.commit()

        db.refresh(

            router,

        )

        return health


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

    @staticmethod
    def list_interfaces(
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

                provider.interfaces.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def get_interface(
        db,
        router_id,
        interface_name,
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

                provider.interfaces.get(

                    api,

                    interface_name,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )
            
    @staticmethod
    def list_interface_statistics(
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

                provider.interfaces.get_all_statistics(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def get_interface_statistics(
        db,
        router_id,
        interface_name,
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

                provider.interfaces.get_statistics(

                    api,

                    interface_name,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )
            
    @staticmethod
    def list_logs(
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

                provider.logs.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def filter_logs(
        db,
        router_id,
        topic=None,
        severity=None,
        date=None,
        search=None,
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

                provider.logs.filter(

                    api,

                    topic=topic,

                    severity=severity,

                    date=date,

                    search=search,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )
            
    @staticmethod
    def list_address_lists(
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

                provider.address_lists.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def get_address_list(
        db,
        router_id,
        address_id,
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

                provider.address_lists.get(

                    api,

                    address_id,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def create_address_list(
        db,
        router_id,
        list_name,
        address,
        comment=None,
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

            provider.address_lists.create(

                api,

                list_name,

                address,

                comment,

            )

            return {

                "success": True,

                "message": (

                    "Address list created "

                    "successfully."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def delete_address_list(
        db,
        router_id,
        address_id,
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

            provider.address_lists.delete(

                api,

                address_id,

            )

            return {

                "success": True,

                "message": (

                    "Address list deleted "

                    "successfully."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

            )
          

    # ==========================================================
    # Firewall
    # ==========================================================

    @staticmethod
    def list_filter_rules(
        db,
        router_id,
    ):

        return RouterService._list_firewall_rules(

            db,

            router_id,

            "get_filter_rules",

        )


    @staticmethod
    def get_filter_rule(
        db,
        router_id,
        rule_id,
    ):

        return RouterService._get_firewall_rule(

            db,

            router_id,

            "get_filter_rule",

            rule_id,

        )


    @staticmethod
    def list_nat_rules(
        db,
        router_id,
    ):

        return RouterService._list_firewall_rules(

            db,

            router_id,

            "get_nat_rules",

        )


    @staticmethod
    def get_nat_rule(
        db,
        router_id,
        rule_id,
    ):

        return RouterService._get_firewall_rule(

            db,

            router_id,

            "get_nat_rule",

            rule_id,

        )


    @staticmethod
    def list_mangle_rules(
        db,
        router_id,
    ):

        return RouterService._list_firewall_rules(

            db,

            router_id,

            "get_mangle_rules",

        )


    @staticmethod
    def get_mangle_rule(
        db,
        router_id,
        rule_id,
    ):

        return RouterService._get_firewall_rule(

            db,

            router_id,

            "get_mangle_rule",

            rule_id,

        )


    @staticmethod
    def list_raw_rules(
        db,
        router_id,
    ):

        return RouterService._list_firewall_rules(

            db,

            router_id,

            "get_raw_rules",

        )


    @staticmethod
    def get_raw_rule(
        db,
        router_id,
        rule_id,
    ):

        return RouterService._get_firewall_rule(

            db,

            router_id,

            "get_raw_rule",

            rule_id,

        )
        
        
    # ==========================================================
    # Queues
    # ==========================================================

    @staticmethod
    def list_simple_queues(
        db,
        router_id,
    ):

        return RouterService._list_queues(

            db,

            router_id,

            "get_simple_queues",

        )


    @staticmethod
    def get_simple_queue(
        db,
        router_id,
        queue_id,
    ):

        return RouterService._get_queue(

            db,

            router_id,

            "get_simple_queue",

            queue_id,

        )


    @staticmethod
    def list_queue_trees(
        db,
        router_id,
    ):

        return RouterService._list_queues(

            db,

            router_id,

            "get_queue_trees",

        )


    @staticmethod
    def get_queue_tree(
        db,
        router_id,
        queue_id,
    ):

        return RouterService._get_queue(

            db,

            router_id,

            "get_queue_tree",

            queue_id,

        )
        
        
    # ==========================================================
    # IP Pools
    # ==========================================================

    @staticmethod
    def list_ip_pools(
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

                provider.ip_pools.get_all(

                    api,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def get_ip_pool(
        db,
        router_id,
        pool_id,
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

                provider.ip_pools.get(

                    api,

                    pool_id,

                )

            )

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def create_ip_pool(
        db,
        router_id,
        name,
        ranges,
        comment=None,
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

            provider.ip_pools.create(

                api,

                name,

                ranges,

                comment,

            )

            return {

                "success": True,

                "message": (

                    "IP pool created "

                    "successfully."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def update_ip_pool(
        db,
        router_id,
        pool_id,
        name,
        ranges,
        comment=None,
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

            pool = (

                provider.ip_pools.find(

                    api,

                    pool_id,

                )

            )

            if pool is None:

                raise ValueError(

                    f"IP Pool "

                    f"'{pool_id}' "

                    "was not found."

                )

            provider.ip_pools.update(

                api,

                pool,

                name,

                ranges,

                comment,

            )

            return {

                "success": True,

                "message": (

                    "IP pool updated "

                    "successfully."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

            )


    @staticmethod
    def delete_ip_pool(
        db,
        router_id,
        pool_id,
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

            pool = (

                provider.ip_pools.find(

                    api,

                    pool_id,

                )

            )

            if pool is None:

                raise ValueError(

                    f"IP Pool "

                    f"'{pool_id}' "

                    "was not found."

                )

            provider.ip_pools.delete(

                api,

                pool,

            )

            return {

                "success": True,

                "message": (

                    "IP pool deleted "

                    "successfully."

                ),

            }

        finally:

            provider.connection.disconnect(

                api,

            )
            
    # ==========================================================
    # DHCP
    # ==========================================================

    @staticmethod
    def list_dhcp_servers(
        db,
        router_id,
    ):

        return RouterService._list_dhcp(

            db,

            router_id,

            "get_servers",

        )


    @staticmethod
    def get_dhcp_server(
        db,
        router_id,
        server_id,
    ):

        return RouterService._get_dhcp(

            db,

            router_id,

            "get_server",

            server_id,

        )


    @staticmethod
    def list_dhcp_networks(
        db,
        router_id,
    ):

        return RouterService._list_dhcp(

            db,

            router_id,

            "get_networks",

        )


    @staticmethod
    def get_dhcp_network(
        db,
        router_id,
        network_id,
    ):

        return RouterService._get_dhcp(

            db,

            router_id,

            "get_network",

            network_id,

        )


    @staticmethod
    def list_dhcp_options(
        db,
        router_id,
    ):

        return RouterService._list_dhcp(

            db,

            router_id,

            "get_options",

        )


    @staticmethod
    def get_dhcp_option(
        db,
        router_id,
        option_id,
    ):

        return RouterService._get_dhcp(

            db,

            router_id,

            "get_option",

            option_id,

        )
        
        
    # ==========================================================
    # DHCP Leases
    # ==========================================================

    @staticmethod
    def list_dhcp_leases(
        db,
        router_id,
    ):

        return (

            RouterService._list_dhcp_leases(

                db,

                router_id,

            )

        )


    @staticmethod
    def get_dhcp_lease(
        db,
        router_id,
        lease_id,
    ):

        return (

            RouterService._get_dhcp_lease(

                db,

                router_id,

                lease_id,

            )

        )
        
    # ==========================================================
    # Hotspot
    # ==========================================================

    @staticmethod
    def list_hotspot_profiles(
        db,
        router_id,
    ):

        return (

            RouterService._list_hotspot(

                db,

                router_id,

                "get_profiles",

            )

        )


    @staticmethod
    def get_hotspot_profile(
        db,
        router_id,
        profile_id,
    ):

        return (

            RouterService._get_hotspot(

                db,

                router_id,

                "get_profile",

                profile_id,

            )

        )


    @staticmethod
    def list_hotspot_servers(
        db,
        router_id,
    ):

        return (

            RouterService._list_hotspot(

                db,

                router_id,

                "get_servers",

            )

        )


    @staticmethod
    def get_hotspot_server(
        db,
        router_id,
        server_id,
    ):

        return (

            RouterService._get_hotspot(

                db,

                router_id,

                "get_server",

                server_id,

            )

        )


    @staticmethod
    def list_hotspot_users(
        db,
        router_id,
    ):

        return (

            RouterService._list_hotspot(

                db,

                router_id,

                "get_users",

            )

        )


    @staticmethod
    def get_hotspot_user(
        db,
        router_id,
        user_id,
    ):

        return (

            RouterService._get_hotspot(

                db,

                router_id,

                "get_user",

                user_id,

            )

        )


    @staticmethod
    def list_hotspot_active(
        db,
        router_id,
    ):

        return (

            RouterService._list_hotspot(

                db,

                router_id,

                "get_active",

            )

        )


    @staticmethod
    def get_hotspot_active_session(
        db,
        router_id,
        session_id,
    ):

        return (

            RouterService._get_hotspot(

                db,

                router_id,

                "get_active_session",

                session_id,

            )

        )

    # ==========================================================
    # Backup
    # ==========================================================

    @staticmethod
    def list_router_files(
        db,
        router_id,
    ):

        return (

            RouterService._list_backup(

                db,

                router_id,

                "get_files",

            )

        )

    @staticmethod
    def get_router_file(
        db,
        router_id,
        file_id,
    ):

        return (

            RouterService._get_backup(

                db,

                router_id,

                "get_file",

                file_id,

            )

        )

    @staticmethod
    def list_backup_schedules(
        db,
        router_id,
    ):

        return (

            RouterService._list_backup(

                db,

                router_id,

                "get_schedules",

            )

        )

    @staticmethod
    def get_backup_schedule(
        db,
        router_id,
        schedule_id,
    ):

        return (

            RouterService._get_backup(

                db,

                router_id,

                "get_schedule",

                schedule_id,

            )

        )

    @staticmethod
    def create_backup(
        db,
        router_id,
        name,
    ):

        return (

            RouterService._execute_backup(

                db,

                router_id,

                "create_backup",

                name,

            )

        )

    @staticmethod
    def create_export(
        db,
        router_id,
        name,
    ):

        return (

            RouterService._execute_backup(

                db,

                router_id,

                "create_export",

                name,

            )

        )