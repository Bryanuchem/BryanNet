from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.device import (
    DeviceCreate,
    DeviceResponse
)

from app.schemas.common import (
    MessageResponse
)

from app.services.device_service import (
    DeviceService
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post(
    "/register",
    response_model=DeviceResponse
)
def register_device(
    device: DeviceCreate,
    db: Session = Depends(get_db)
):

    return DeviceService.register_device(
        db=db,
        customer_id=device.customer_id,
        device_name=device.device_name,
        mac_address=device.mac_address
    )
    
@router.get(
    "/{customer_id}",
    response_model=list[DeviceResponse]
)



def get_customer_devices(
    customer_id: int,
    db: Session = Depends(get_db)
):

    return DeviceService.get_customer_devices(
        db=db,
        customer_id=customer_id
    )
    
@router.delete(
    "/{device_id}",
    response_model=MessageResponse
)

def remove_device(
    device_id: int,
    db: Session = Depends(get_db)
):

    return DeviceService.remove_device(
        db=db,
        device_id=device_id
    )