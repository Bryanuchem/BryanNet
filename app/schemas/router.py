from pydantic import BaseModel

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

    management_ip: IPv4Address

    location_name: LocationName

    provider: RouterProviderType


# ==========================================================
# Response Schemas
# ==========================================================

class RouterResponse(BaseModel):

    router_id: int

    router_name: str

    management_ip: str

    location_name: str

    router_type: RouterProviderType

    status: RouterStatus

    class Config:

        from_attributes = True