from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.schemas.common import (
    MessageResponse,
)

from app.schemas.device import (
    DeviceCreate,
    DeviceRenameRequest,
    DeviceReplacementRequest,
    DeviceResponse,
)

from app.services.device_service import (
    DeviceService,
)


router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/register",
    response_model=DeviceResponse,
)
def register_device(
    device: DeviceCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.register_device(
            db=db,
            customer_id=device.customer_id,
            device_name=device.device_name,
            mac_address=device.mac_address,
        )
    )


@router.patch(
    "/{device_id}/activate",
    response_model=DeviceResponse,
)
def activate_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.activate_device(
            db=db,
            device_id=device_id,
        )
    )


@router.patch(
    "/{device_id}/deactivate",
    response_model=DeviceResponse,
)
def deactivate_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.deactivate_device(
            db=db,
            device_id=device_id,
        )
    )


@router.patch(
    "/{device_id}/approve",
    response_model=DeviceResponse,
)
def approve_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.approve_device(
            db=db,
            device_id=device_id,
        )
    )


@router.patch(
    "/{device_id}/block",
    response_model=DeviceResponse,
)
def block_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.block_device(
            db=db,
            device_id=device_id,
        )
    )


@router.patch(
    "/{device_id}/rename",
    response_model=DeviceResponse,
)
def rename_device(
    device_id: int,
    request: DeviceRenameRequest,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.rename_device(
            db=db,
            device_id=device_id,
            device_name=request.device_name,
        )
    )


@router.post(
    "/replace",
    response_model=DeviceResponse,
)
def replace_device(
    request: DeviceReplacementRequest,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.replace_device(
            db=db,
            customer_id=request.customer_id,
            old_device_id=request.old_device_id,
            new_device_id=request.new_device_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[DeviceResponse],
)
def get_all_devices(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.get_all_devices(
            db,
        )
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
)
def get_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.get_device(
            db=db,
            device_id=device_id,
        )
    )


@router.get(
    "/customer/{customer_id}",
    response_model=list[DeviceResponse],
)
def get_customer_devices(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.get_customer_devices(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/customer/{customer_id}/active",
    response_model=list[DeviceResponse],
)
def get_active_devices(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        DeviceService.get_active_devices(
            db=db,
            customer_id=customer_id,
        )
    )