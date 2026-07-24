from enum import (
    Enum,
)


class SessionType(
    str,
    Enum,
):

    # ==========================================================
    # Session Types
    # ==========================================================

    HOTSPOT = (
        "hotspot"
    )

    PPP = (
        "ppp"
    )

    DHCP = (
        "dhcp"
    )

    VPN = (
        "vpn"
    )