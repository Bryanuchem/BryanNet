from app.database.database import (
    SessionLocal,
)

from app.providers.router.factory import (
    ProviderFactory,
)

from app.services.router_service import (
    RouterService,
)


# ==========================================================
# Helpers
# ==========================================================

def print_section(
    title,
    resource,
):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)

    found = False

    for item in resource:

        found = True

        print(item)

    if not found:

        print()

        print(
            "No entries found."
        )


# ==========================================================
# Main
# ==========================================================

db = SessionLocal()

router = RouterService.get_router(

    db,

    3,

)

provider = ProviderFactory.get(

    router,

)

api = None

try:

    api = provider.connection.connect(

        router,

    )

    # ======================================================
    # System
    # ======================================================

    print_section(

        "System Resource",

        provider.connection.path(

            api,

            "system",

            "resource",

        ),

    )

    print_section(

        "Router Files",

        provider.connection.path(

            api,

            "file",

        ),

    )

    print_section(

        "System Scheduler",

        provider.connection.path(

            api,

            "system",

            "scheduler",

        ),

    )

    print_section(

        "Interfaces",

        provider.connection.path(

            api,

            "interface",

        ),

    )

    # ======================================================
    # Addressing
    # ======================================================

    print_section(

        "IP Addresses",

        provider.connection.path(

            api,

            "ip",

            "address",

        ),

    )

    print_section(

        "IP Pools",

        provider.connection.path(

            api,

            "ip",

            "pool",

        ),

    )

    # ======================================================
    # DHCP
    # ======================================================

    print_section(

        "DHCP Servers",

        provider.connection.path(

            api,

            "ip",

            "dhcp-server",

        ),

    )

    print_section(

        "DHCP Networks",

        provider.connection.path(

            api,

            "ip",

            "dhcp-server",

            "network",

        ),

    )

    print_section(

        "DHCP Leases",

        provider.connection.path(

            api,

            "ip",

            "dhcp-server",

            "lease",

        ),

    )

    # ======================================================
    # Hotspot
    # ======================================================

    print_section(

        "Hotspot",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

        ),

    )

    print_section(

        "Hotspot Profiles",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "profile",

        ),

    )

    print_section(

        "Hotspot User Profiles",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "user",

            "profile",

        ),

    )

    print_section(

        "Hotspot Users",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "user",

        ),

    )

    print_section(

        "Hotspot Active",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "active",

        ),

    )

    print_section(

        "Hotspot Hosts",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "host",

        ),

    )

    print_section(

        "Hotspot Cookies",

        provider.connection.path(

            api,

            "ip",

            "hotspot",

            "cookie",

        ),

    )

    # ======================================================
    # PPP
    # ======================================================

    print_section(

        "PPP Profiles",

        provider.connection.path(

            api,

            "ppp",

            "profile",

        ),

    )

    print_section(

        "PPP Secrets",

        provider.connection.path(

            api,

            "ppp",

            "secret",

        ),

    )

    print_section(

        "PPP Active",

        provider.connection.path(

            api,

            "ppp",

            "active",

        ),

    )

    # ======================================================
    # Firewall
    # ======================================================

    print_section(

        "Firewall Filter",

        provider.connection.path(

            api,

            "ip",

            "firewall",

            "filter",

        ),

    )

    print_section(

        "Firewall NAT",

        provider.connection.path(

            api,

            "ip",

            "firewall",

            "nat",

        ),

    )

    print_section(

        "Firewall Mangle",

        provider.connection.path(

            api,

            "ip",

            "firewall",

            "mangle",

        ),

    )

    print_section(

        "Firewall Raw",

        provider.connection.path(

            api,

            "ip",

            "firewall",

            "raw",

        ),

    )

    print_section(

        "Address Lists",

        provider.connection.path(

            api,

            "ip",

            "firewall",

            "address-list",

        ),

    )

    # ======================================================
    # Queues
    # ======================================================

    print_section(

        "Simple Queues",

        provider.connection.path(

            api,

            "queue",

            "simple",

        ),

    )

    print_section(

        "Queue Trees",

        provider.connection.path(

            api,

            "queue",

            "tree",

        ),

    )

    print_section(

        "Users",

        provider.connection.path(

            api,

            "user",

        ),

    )

    print_section(

        "User Groups",

        provider.connection.path(

            api,

            "user",

            "group",

        ),

)
    
    print_section(

        "Identity",

        provider.connection.path(

            api,

            "system",

            "identity",

        ),

    )

finally:

    provider.connection.disconnect(

        api,

    )

    db.close()