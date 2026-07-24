from typing import Optional

from pydantic import BaseModel

from app.schemas.types import IPv4Address


# ==========================================================
# Request Schemas
# ==========================================================

class RouterEventCreate(BaseModel):

    event: str

    router_identifier: str

    router_secret: str

    router_time: str

    username: Optional[str] = None

    mac_address: Optional[str] = None

    ip_address: Optional[IPv4Address] = None

    login_by: Optional[str] = None

    bytes_in: Optional[int] = None

    bytes_out: Optional[int] = None

    packets_in: Optional[int] = None

    packets_out: Optional[int] = None

    disconnect_reason: Optional[str] = None

    reason: Optional[str] = None