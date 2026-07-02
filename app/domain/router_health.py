from dataclasses import dataclass


@dataclass(slots=True)
class RouterHealth:

    healthy: bool

    connected: bool

    latency_ms: float | None

    router_os_version: str | None

    message: str