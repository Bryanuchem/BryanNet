from pydantic import BaseModel

from datetime import datetime

from app.enums import (
    RouterProviderType,
    RouterStatus,
)

from app.schemas.types import (
    IPv4Address,
    LocationName,
    RouterName,
)


# ==========================================================
# Request Schemas
# ==========================================================

class RouterCreate(BaseModel):

    router_name: RouterName

    hostname: str

    location_name: LocationName

    router_type: RouterProviderType

    api_port: int = 8728

    api_username: str

    api_password: str

    use_ssl: bool = False

    connection_timeout: int = 10

class RouterUpdate(BaseModel):

    router_name: RouterName

    hostname: str

    location_name: LocationName

    router_type: RouterProviderType

    api_port: int

    api_username: str

    api_password: str | None = None

    use_ssl: bool

    connection_timeout: int
    
class RouterRead(BaseModel):

    router_id: int

    router_name: str

    hostname: str

    location_name: str

    router_type: RouterProviderType

    status: RouterStatus

    api_port: int

    api_username: str

    use_ssl: bool

    connection_timeout: int

    last_health_check: datetime | None

    last_latency_ms: float | None

    router_os_version: str | None

    class Config:

        from_attributes = True

# ==========================================================
# Response Schemas
# ==========================================================

class RouterResponse(BaseModel):

    router_id: int

    router_name: str

    hostname: str

    location_name: str

    router_type: RouterProviderType

    status: RouterStatus
    
    api_port: int

    api_username: str

    use_ssl: bool

    connection_timeout: int

    last_health_check: datetime | None

    last_latency_ms: float | None

    router_os_version: str | None

    class Config:

        from_attributes = True