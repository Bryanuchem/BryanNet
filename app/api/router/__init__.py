from fastapi import (
    FastAPI,
)

from .router import (
    router as router_router,
)

from .runtime import (
    router as router_runtime_router,
)

from .account_runtime import (
    router as router_account_runtime_router,
)

from .profile import (
    router as router_profile_router,
)

from .secret import (
    router as router_secret_router,
)

from .session import (
    router as router_session_router,
)

from .interface import (
    router as router_interface_router,
)

from .logs import (
    router as router_logs_router,
)

from .address_lists import (
    router as router_address_lists_router,
)

from .firewall import (
    router as router_firewall_router,
)

from .queues import (
    router as router_queues_router,
)

from .ip_pools import (
    router as router_ip_pools_router,
)

from .dhcp import (
    router as router_dhcp_router,
)

from .hotspot import (
    router as router_hotspot_router,
)

from .backup import (
    router as router_backup_router,
)

from .operations import (
    router as router_operations_router,
)

from app.api.router.events import (
    router as router_events_router,
)

def register(
    app: FastAPI,
):

    app.include_router(
        router_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_runtime_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_account_runtime_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_profile_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_secret_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_session_router,
        prefix="/api/v1",
    )

    app.include_router(
        router_interface_router,
    )

    app.include_router(
        router_logs_router,
    )

    app.include_router(
        router_address_lists_router,
    )

    app.include_router(
        router_firewall_router,
    )

    app.include_router(
        router_queues_router,
    )

    app.include_router(
        router_ip_pools_router,
    )

    app.include_router(
        router_dhcp_router,
    )

    app.include_router(
        router_hotspot_router,
    )

    app.include_router(
        router_backup_router,
    )
    
    app.include_router(
        router_operations_router,
        prefix="/api/v1",
    )
    
    app.include_router(
        router_events_router,
        prefix="/api/v1",
    )