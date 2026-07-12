from datetime import datetime

from pydantic import BaseModel

from app.enums import DeviceStatus


# ==========================================================
# Portal Device Response
# ==========================================================

class PortalDeviceResponse(BaseModel):

    device_id: int

    device_name: str | None

    mac_address: str

    device_type: str

    device_status: DeviceStatus

    first_seen: datetime | None

    last_seen: datetime | None

    model_config = {
        "from_attributes": True,
    }


# ==========================================================
# Portal Device List Response
# ==========================================================

class PortalDeviceListResponse(BaseModel):

    allowed_devices: int

    active_devices: int

    available_slots: int

    devices: list[PortalDeviceResponse]


# ==========================================================
# Portal Device Action Request
# ==========================================================

class PortalDeviceActionRequest(BaseModel):

    telegram_user_id: int

    device_name: str | None = None