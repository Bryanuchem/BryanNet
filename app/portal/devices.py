from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.portal_device import (
    PortalDeviceActionRequest,
    PortalDeviceListResponse,
)

from app.services.portal.device_service import (
    PortalDeviceService,
)

router = APIRouter(
    prefix="/devices",
    tags=["Portal Devices"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/{telegram_user_id}",
    response_model=PortalDeviceListResponse,
)
def get_customer_devices(
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.get_customer_devices(
            db,
            telegram_user_id,
        )
    )


# ==========================================================
# Business Commands
# ==========================================================

@router.patch(
    "/{device_id}/rename",
    response_model=PortalDeviceListResponse,
)
def rename_device(
    device_id: int,
    request: PortalDeviceActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.rename_device(
            db,
            device_id,
            request,
        )
    )


@router.patch(
    "/{device_id}/activate",
    response_model=PortalDeviceListResponse,
)
def activate_device(
    device_id: int,
    request: PortalDeviceActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.activate_device(
            db,
            device_id,
            request,
        )
    )


@router.patch(
    "/{device_id}/deactivate",
    response_model=PortalDeviceListResponse,
)
def deactivate_device(
    device_id: int,
    request: PortalDeviceActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.deactivate_device(
            db,
            device_id,
            request,
        )
    )


@router.patch(
    "/{device_id}/block",
    response_model=PortalDeviceListResponse,
)
def block_device(
    device_id: int,
    request: PortalDeviceActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.block_device(
            db,
            device_id,
            request,
        )
    )


@router.patch(
    "/{device_id}/unblock",
    response_model=PortalDeviceListResponse,
)
def unblock_device(
    device_id: int,
    request: PortalDeviceActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalDeviceService.unblock_device(
            db,
            device_id,
            request,
        )
    )