from datetime import datetime

from pydantic import BaseModel

from app.enums import (
    DeviceStatus,
)

from app.schemas.types import (
    DeviceName,
    MacAddress,
    PositiveInt,
)


class DeviceCreate(BaseModel):

    customer_id: PositiveInt

    device_name: DeviceName

    mac_address: MacAddress


class DeviceRenameRequest(BaseModel):

    device_name: DeviceName


class DeviceReplacementRequest(BaseModel):

    customer_id: PositiveInt

    old_device_id: PositiveInt

    new_device_id: PositiveInt


class DeviceResponse(BaseModel):

    device_id: int

    customer_id: int
    
    customer_name: str

    device_name: str

    mac_address: str

    device_status: DeviceStatus

    class Config:

        from_attributes = True
        
class DeviceListItem(BaseModel):

    device_id: int

    customer_id: int
    
    customer_name: str

    device_name: str | None = None

    mac_address: str

    device_status: DeviceStatus

    approved_by_customer: bool

    first_seen: datetime | None = None

    last_seen: datetime | None = None

    class Config:

        from_attributes = True