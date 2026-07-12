from fastapi import (
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.enums import (
    DeviceStatus,
)

from app.models.device import (
    Device,
)

from app.schemas.portal_device import (
    PortalDeviceActionRequest,
    PortalDeviceListResponse,
    PortalDeviceResponse,
)

from app.services.customer_service import (
    CustomerService,
)

from app.services.device_service import (
    DeviceService,
)

from app.services.plan_service import (
    PlanService,
)

from app.services.subscription_service import (
    SubscriptionService,
)


class PortalDeviceService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_customer(
        db: Session,
        telegram_user_id: int,
    ):

        customer = (
            CustomerService.get_customer_by_telegram_id(
                db,
                telegram_user_id,
            )
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        return customer

    @staticmethod
    def _get_customer_device(
        db: Session,
        customer,
        device_id: int,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        if (
            device.customer_id
            != customer.customer_id
        ):

            raise HTTPException(
                status_code=404,
                detail="Device not found.",
            )

        return device

    @staticmethod
    def _build_device_response(
        device: Device,
    ):

        return PortalDeviceResponse.model_validate(
            device,
        )

    @staticmethod
    def _build_device_list_response(
        db: Session,
        customer,
    ):

        devices = (
            DeviceService.get_customer_devices(
                db,
                customer.customer_id,
            )
        )

        active_devices = sum(

            1

            for device in devices

            if (
                device.device_status
                == DeviceStatus.ACTIVE
            )

        )

        subscription = (
            SubscriptionService.get_active_subscription(
                db,
                customer.customer_id,
            )
        )

        allowed_devices = 0

        if subscription:

            plan = (
                PlanService.get_plan(
                    db,
                    subscription.plan_id,
                )
            )

            allowed_devices = (
                plan.max_devices
            )

        available_slots = max(
            0,
            allowed_devices
            - active_devices,
        )

        return PortalDeviceListResponse(

            allowed_devices=allowed_devices,

            active_devices=active_devices,

            available_slots=available_slots,

            devices=[
                PortalDeviceService
                ._build_device_response(
                    device,
                )

                for device in devices
            ],

        )

    # ==========================================================
    # Public Methods
    # ==========================================================
    
    @staticmethod
    def get_customer_devices(
        db: Session,
        telegram_user_id: int,
    ):

        customer = (
            PortalDeviceService._get_customer(
                db,
                telegram_user_id,
            )
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )

    @staticmethod
    def rename_device(
        db: Session,
        device_id: int,
        request: PortalDeviceActionRequest,
    ):

        if not request.device_name:

            raise HTTPException(
                status_code=400,
                detail="Device name is required.",
            )
            
        customer = (
            PortalDeviceService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        device = (
            PortalDeviceService
            ._get_customer_device(
                db,
                customer,
                device_id,
            )
        )

        DeviceService._set_device_name(
            db,
            device,
            request.device_name,
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )

    @staticmethod
    def activate_device(
        db: Session,
        device_id: int,
        request: PortalDeviceActionRequest,
    ):

        customer = (
            PortalDeviceService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        device = (
            PortalDeviceService
            ._get_customer_device(
                db,
                customer,
                device_id,
            )
        )

        DeviceService._set_device_active(
            db,
            device,
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )

    @staticmethod
    def deactivate_device(
        db: Session,
        device_id: int,
        request: PortalDeviceActionRequest,
    ):

        customer = (
            PortalDeviceService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        device = (
            PortalDeviceService
            ._get_customer_device(
                db,
                customer,
                device_id,
            )
        )

        DeviceService._set_device_inactive(
            db,
            device,
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )

    @staticmethod
    def block_device(
        db: Session,
        device_id: int,
        request: PortalDeviceActionRequest,
    ):

        customer = (
            PortalDeviceService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        device = (
            PortalDeviceService
            ._get_customer_device(
                db,
                customer,
                device_id,
            )
        )

        DeviceService._set_device_blocked(
            db,
            device,
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )

    @staticmethod
    def unblock_device(
        db: Session,
        device_id: int,
        request: PortalDeviceActionRequest,
    ):

        customer = (
            PortalDeviceService._get_customer(
                db,
                request.telegram_user_id,
            )
        )

        device = (
            PortalDeviceService
            ._get_customer_device(
                db,
                customer,
                device_id,
            )
        )

        DeviceService._set_device_unblocked(
            db,
            device,
        )

        return (
            PortalDeviceService
            ._build_device_list_response(
                db,
                customer,
            )
        )