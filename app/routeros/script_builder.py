from __future__ import annotations

from .templates import (
    fetch_template,
    globals_template,
    join_sections,
    json_payload_template,
    log_payload_template,
    login_context_template,
    login_error_context_template,
    logout_context_template,
    router_time_template,
    script_header,
)


def build_login_script() -> str:
    return join_sections(
        script_header("BryanNet Hotspot Login"),
        globals_template(),
        login_context_template(),
        router_time_template(),
        json_payload_template(
            "event",
            {
                "event": "hotspot.login",
                "router_identifier": "$BNRouterIdentifier",
                "router_secret": "$BNRouterSecret",
                "username": "$username",
                "mac_address": "$mac",
                "ip_address": "$ip",
                "login_by": "$loginBy",
                "router_time": "$routerTime",
            },
        ),
        log_payload_template(),
        fetch_template(),
    )


def build_logout_script() -> str:
    return join_sections(
        script_header("BryanNet Hotspot Logout"),
        globals_template(),
        logout_context_template(),
        router_time_template(),
        json_payload_template(
            "event",
            {
                "event": "hotspot.logout",
                "router_identifier": "$BNRouterIdentifier",
                "router_secret": "$BNRouterSecret",
                "username": "$username",
                "mac_address": "$mac",
                "ip_address": "$ip",
                "bytes_in": "0",
                "bytes_out": "0",
                "packets_in": "0",
                "packets_out": "0",
                "disconnect_reason": "logout",
                "router_time": "$routerTime",
            },
        ),
        log_payload_template(),
        fetch_template(),
    )


def build_login_error_script() -> str:
    return join_sections(
        script_header("BryanNet Hotspot Login Error"),
        globals_template(),
        login_error_context_template(),
        router_time_template(),
        json_payload_template(
            "event",
            {
                "event": "hotspot.login_error",
                "router_identifier": "$BNRouterIdentifier",
                "router_secret": "$BNRouterSecret",
                "username": "$username",
                "mac_address": "$mac",
                "reason": "authentication_failed",
                "router_time": "$routerTime",
            },
        ),
        log_payload_template(),
        fetch_template(),
    )


def build_daily_cleanup_script() -> str:
    return join_sections(
        script_header("BryanNet Daily Cleanup"),
        globals_template(),
        router_time_template(),
        json_payload_template(
            "event",
            {
                "event": "router.daily_cleanup",
                "router_identifier": "$BNRouterIdentifier",
                "router_secret": "$BNRouterSecret",
                "router_time": "$routerTime",
            },
        ),
        log_payload_template(),
        fetch_template(),
    )