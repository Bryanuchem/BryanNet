from enum import (
    Enum,
)


class RouterEventType(
    str,
    Enum,
):

    # ==========================================================
    # Hotspot
    # ==========================================================

    HOTSPOT_LOGIN = (
        "hotspot.login"
    )

    HOTSPOT_LOGOUT = (
        "hotspot.logout"
    )

    HOTSPOT_LOGIN_ERROR = (
        "hotspot.login_error"
    )

    # ==========================================================
    # PPP
    # ==========================================================

    PPP_LOGIN = (
        "ppp.login"
    )

    PPP_LOGOUT = (
        "ppp.logout"
    )

    # ==========================================================
    # DHCP
    # ==========================================================

    DHCP_LEASE = (
        "dhcp.lease"
    )

    DHCP_RELEASE = (
        "dhcp.release"
    )

    # ==========================================================
    # VPN
    # ==========================================================

    VPN_LOGIN = (
        "vpn.login"
    )

    VPN_LOGOUT = (
        "vpn.logout"
    )
    
    
    # ==========================================================
    # Router
    # ==========================================================

    ROUTER_DAILY_CLEANUP = (
        "router.daily_cleanup"
    )