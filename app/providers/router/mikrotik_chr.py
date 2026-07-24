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

from app.providers.router.mikrotik_interface_repository import (
    MikroTikInterfaceRepository,
)

from app.providers.router.mikrotik_log_repository import (
    MikroTikLogRepository,
)

from app.providers.router.mikrotik_address_list_repository import (
    MikroTikAddressListRepository,
)

from app.providers.router.mikrotik_firewall_repository import (
    MikroTikFirewallRepository,
)

from app.providers.router.mikrotik_queue_repository import (
    MikroTikQueueRepository,
)

from app.providers.router.mikrotik_ip_pool_repository import (
    MikroTikIPPoolRepository,
)

from app.providers.router.mikrotik_dhcp_repository import (
    MikroTikDHCPRepository,
)

from app.providers.router.mikrotik_dhcp_lease_repository import (
    MikroTikDHCPLeaseRepository,
)

from app.providers.router.mikrotik_hotspot_repository import (
    MikroTikHotspotRepository,
)

from app.providers.router.mikrotik_hotspot_user_profile_repository import (
    MikroTikHotspotUserProfileRepository,
)

from app.services.router_access_service import (
    RouterAccessService,
)

from app.providers.router.mikrotik_backup_repository import (
    MikroTikBackupRepository,
)

from app.providers.router.mikrotik_script_repository import (
    MikroTikScriptRepository,
)

from app.providers.router.mikrotik_scheduler_repository import (
    MikroTikSchedulerRepository,
)

from app.providers.router.mikrotik_hotspot_walled_garden_repository import (
    MikroTikHotspotWalledGardenRepository,
)

from app.core.settings import (
    settings,
)

from app.services.hotspot_desired_state_service import (
    HotspotDesiredStateService,
)

from app.routeros import (
    LOGIN_SCRIPT,
    LOGOUT_SCRIPT,
    LOGIN_ERROR_SCRIPT,
    DAILY_CLEANUP_SCRIPT,
    LOGIN_SCRIPT_NAME,
    LOGOUT_SCRIPT_NAME,
    LOGIN_ERROR_SCRIPT_NAME,
    DAILY_CLEANUP_SCRIPT_NAME,
    DAILY_CLEANUP_SCHEDULER,
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

        self.api = None

        self.persistent_connection = False

        self.profiles = (
            MikroTikProfileRepository()
        )

        self.secrets = (
            MikroTikSecretRepository()
        )

        self.sessions = (
            MikroTikSessionRepository()
        )

        self.interfaces = (

            MikroTikInterfaceRepository()

        )

        self.logs = (

            MikroTikLogRepository()

        )

        self.address_lists = (

            MikroTikAddressListRepository()

        )
        
        self.firewall = (

            MikroTikFirewallRepository()

        )

        self.queues = (

            MikroTikQueueRepository()

        )
        
        self.ip_pools = (

            MikroTikIPPoolRepository()

        )
        
        self.dhcp = (

            MikroTikDHCPRepository()

        )
        
        self.dhcp_leases = (

            MikroTikDHCPLeaseRepository()

        )
        
        self.hotspot = (

            MikroTikHotspotRepository()

        )

        self.hotspot_profiles = (
            
            MikroTikHotspotUserProfileRepository()
            
        )

        self.scripts = (
            MikroTikScriptRepository()
        )

        self.schedulers = (
            MikroTikSchedulerRepository()
        )

        self.backups = (

            MikroTikBackupRepository()

        )

        self.hotspot_walled_garden = (

            MikroTikHotspotWalledGardenRepository()

        )
        
    # ==========================================================
    # Bootstrap Helpers
    # ==========================================================
 
    def _ensure_hotspot_profiles(
        self,
        api,
        profiles,
    ):

        for profile in profiles:

            self._ensure_hotspot_profile(
                api,
                profile,
            )
 
    def _ensure_hotspot_profile(
        self,
        api,
        profile,
    ):

        existing = (

            self.hotspot_profiles

            .find(

                api,

                profile["name"],

            )

        )

        if not existing:

            self.hotspot_profiles.create(

                api,

                profile,

            )

            return

        self.hotspot_profiles.update(

            api,

            existing,

            profile,

        )
        
    def _ensure_script(
        self,
        api,
        router,
        name,
        source,
    ):

        source = (

            source

            .replace(
                "__BN_API_URL__",
                settings.router_event_url,
            )

            .replace(
                "ROUTER-001",
                router.router_identifier,
            )

            .replace(
                "GENERATED_SECRET",
                router.router_secret,
            )

        )

        existing = (

            self.scripts

            .find(

                api,

                name,

            )

        )

        if not existing:

            self.scripts.create(

                api,

                name=name,

                source=source,

            )

            return

        self.scripts.update(

            api,

            existing,

            source=source,

        )

    def _ensure_scheduler(
        self,
        api,
        scheduler,
    ):

        existing = (

            self.schedulers

            .find(

                api,

                scheduler["name"],

            )

        )

        if not existing:

            self.schedulers.create(

                api,

                scheduler,

            )

            return

        self.schedulers.update(

            api,

            existing,

            scheduler,

        )

    def _ensure_hotspot_walled_garden(
        self,
        api,
    ):

        self.hotspot_walled_garden.ensure(

            api,

            dst_host=settings.portal_backend_host,

            dst_port=settings.portal_backend_port,

            comment="BryanNet Portal",

        )
    
    # ==========================================================
    # Bootstrap
    # ==========================================================

    def ensure_router_bootstrap(
        self,
        db,
        router,
    ):

        api = None

        try:

            api = (

                self.connection.connect(

                    router,

                )

            )

            self._ensure_script(

                api,

                router,

                LOGIN_SCRIPT_NAME,

                LOGIN_SCRIPT,

            )

            self._ensure_script(

                api,

                router,

                LOGOUT_SCRIPT_NAME,

                LOGOUT_SCRIPT,

            )

            self._ensure_script(

                api,

                router,

                LOGIN_ERROR_SCRIPT_NAME,

                LOGIN_ERROR_SCRIPT,

            )

            self._ensure_script(

                api,

                router,

                DAILY_CLEANUP_SCRIPT_NAME,

                DAILY_CLEANUP_SCRIPT,

            )

            self._ensure_scheduler(

                api,

                DAILY_CLEANUP_SCHEDULER,

            )

            self._ensure_hotspot_walled_garden(

                api,

            )

        finally:

            self.connection.disconnect(

                api,

            )
    
    # ==========================================================
    # Hotspot Desired State
    # ==========================================================

    def synchronize_hotspot(
        self,
        api,
    ):

        return (

            HotspotDesiredStateService.synchronize(

                api,

            )

        )


    def verify_hotspot(
        self,
        api,
    ):

        return (

            HotspotDesiredStateService.verify_state(

                api,

            )

        )

    # ==========================================================
    # Customer Synchronization
    # ==========================================================

    def synchronize_customer(
        self,
        db,
        context: RouterContext,
    ):

        print("Entered MikroTik provider")

        api = None

        try:

            api = (

                self.connection

                .connect(

                    context.router,

                )

            )

            # Customer profile synchronization binds the named
            # on-logout hook below. Ensure the target script exists
            # on this router in the same normal provisioning flow.
            self._ensure_script(

                api,

                context.router,

                LOGOUT_SCRIPT_NAME,

                LOGOUT_SCRIPT,

            )

            user = (

                RouterAccessService

                .ensure_access(

                    api,

                    context,

                )

            )

            if (

                not context.router_account.is_enabled

            ):

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

            #
            # Disconnect only the active runtime session.
            #
            # Do NOT disable the customer's credential.
            #

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
