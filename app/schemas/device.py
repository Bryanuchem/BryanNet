from pydantic import BaseModel


class DeviceCreate(BaseModel):
    customer_id: int
    device_name: str
    mac_address: str


class DeviceRenameRequest(BaseModel):
    device_name: str


class DeviceReplacementRequest(BaseModel):
    customer_id: int
    old_device_id: int
    new_device_id: int


class DeviceResponse(BaseModel):
    device_id: int
    customer_id: int
    customer_name: str
    device_name: str
    mac_address: str
    device_status: str

    class Config:
        from_attributes = True