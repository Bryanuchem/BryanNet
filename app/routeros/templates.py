from __future__ import annotations

from collections.abc import Mapping

from .serializer import serialize_json


def script_header(title: str) -> str:
    return f"""
# ==========================================================
# {title}
# ==========================================================
""".strip()


def globals_template() -> str:
    return """
:global BNApiUrl "__BN_API_URL__"
:global BNRouterIdentifier "ROUTER-001"
:global BNRouterSecret "GENERATED_SECRET"
""".strip()


def router_time_template() -> str:
    return """
:local routerTime [/system clock get date]
:set routerTime ($routerTime . " " . [/system clock get time])
""".strip()


def login_context_template() -> str:
    return """
:local username $"user"
:local mac $"mac-address"
:local ip $"address"
:local loginBy $"login-by"
""".strip()


def logout_context_template() -> str:
    return """
:local username $"user"
:local mac $"mac-address"
:local ip $"address"
""".strip()


def login_error_context_template() -> str:
    return """
:local username $"user"
:local mac $"mac-address"
""".strip()


def json_payload_template(
    event_variable: str,
    fields: Mapping[str, str],
) -> str:
    return serialize_json(
        variable_name=event_variable,
        fields=fields,
    )


def log_payload_template() -> str:
    return ':log warning ("PAYLOAD=" . $payload)'


def fetch_template() -> str:
    return """
/tool fetch \
url=$BNApiUrl \
http-method=post \
http-header-field="Content-Type: application/json" \
http-data=$payload \
keep-result=no
""".strip()


def join_sections(*sections: str) -> str:
    """
    Join non-empty RouterOS sections with a blank line.
    """

    return "\n\n".join(
        section.strip()
        for section in sections
        if section and section.strip()
    )