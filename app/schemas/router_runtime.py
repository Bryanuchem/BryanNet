from pydantic import (
    BaseModel,
)


class RouterHealthResponse(
    BaseModel,
):

    healthy: bool

    connected: bool

    latency_ms: float | None

    router_os_version: str | None

    message: str


class RouterProfileResponse(
    BaseModel,
):

    id: str

    name: str

    rate_limit: str | None


class RouterSecretResponse(
    BaseModel,
):

    id: str

    username: str

    profile: str | None

    disabled: bool


class RouterSessionResponse(
    BaseModel,
):

    id: str

    username: str

    address: str | None

    uptime: str | None