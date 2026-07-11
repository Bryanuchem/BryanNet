from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.device import (
    DeviceCreate,
    DeviceListItem,
    DeviceRenameRequest,
    DeviceReplacementRequest,
    DeviceResponse,
)

from app.services.device_service import (
    DeviceService,
)

from app.enums import DeviceStatus

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_REGISTER,
        ),
    ),
):

    return (
        DeviceService.register_device(
            db=db,
            customer_id=device.customer_id,
            device_name=device.device_name,
            mac_address=device.mac_address,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_ACTIVATE,
        ),
    ),
):

    return (
        DeviceService.activate_device(
            db=db,
            device_id=device_id,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_DEACTIVATE,
        ),
    ),
):

    return (
        DeviceService.deactivate_device(
            db=db,
            device_id=device_id,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_APPROVE,
        ),
    ),
):

    return (
        DeviceService.approve_device(
            db=db,
            device_id=device_id,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_BLOCK,
        ),
    ),
):

    return (
        DeviceService.block_device(
            db=db,
            device_id=device_id,
            admin_id=admin.admin_user_id,
        )
    )


@router.patch(
    "/{device_id}/unblock",
    response_model=DeviceResponse,
)
def unblock_device(
    device_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.DEVICES_UNBLOCK,
        ),
    ),
):

    return (
        DeviceService.unblock_device(
            db=db,
            device_id=device_id,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_RENAME,
        ),
    ),
):

    return (
        DeviceService.rename_device(
            db=db,
            device_id=device_id,
            device_name=request.device_name,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_REPLACE,
        ),
    ),
):

    return (
        DeviceService.replace_device(
            db=db,
            customer_id=request.customer_id,
            old_device_id=request.old_device_id,
            new_device_id=request.new_device_id,
            admin_id=admin.admin_user_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        DeviceListItem,
    ],
)
def get_all_devices(

    search: str | None = None,

    customer_id: int | None = None,

    device_status: DeviceStatus | None = None,

    sort_by: str = "device_id",

    sort_order: str = "asc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.DEVICES_VIEW,
        ),
    ),

):

    return (
        DeviceService.get_all_devices(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

            customer_id=customer_id,

            device_status=device_status,

            sort_by=sort_by,

            sort_order=sort_order,

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
    _=Depends(
        require_permission(
            Permissions.DEVICES_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.DEVICES_VIEW,
        ),
    ),
):

    return (
        DeviceService.get_active_devices(
            db=db,
            customer_id=customer_id,
        )
    )