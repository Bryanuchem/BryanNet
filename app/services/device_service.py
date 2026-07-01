from datetime import datetime

from fastapi import HTTPException

from app.enums import DeviceStatus

from app.models.customer import Customer
from app.models.device import Device
from app.models.plan import Plan

from app.services.subscription_service import (
    SubscriptionService,
)


class DeviceService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_device(
        db,
        device_id,
    ):

        device = (
            db.query(Device)
            .filter(
                Device.device_id == device_id
            )
            .first()
        )

        if not device:

            raise HTTPException(
                status_code=404,
                detail="Device not found.",
            )

        return device

    @staticmethod
    def _find_device_by_mac(
        db,
        mac_address,
    ):

        return (
            db.query(Device)
            .filter(
                Device.mac_address == mac_address
            )
            .first()
        )

    @staticmethod
    def _get_active_subscription(
        db,
        customer_id,
    ):

        subscription = (
            SubscriptionService
            .get_active_subscription(
                db,
                customer_id,
            )
        )

        if not subscription:

            raise HTTPException(
                status_code=400,
                detail="Customer has no active subscription.",
            )

        return subscription

    @staticmethod
    def _validate_device_limit(
        db,
        customer_id,
        plan,
    ):

        active_devices = (
            db.query(Device)
            .filter(
                Device.customer_id == customer_id,
                Device.device_status == DeviceStatus.ACTIVE,
            )
            .count()
        )

        if active_devices >= plan.max_devices:

            raise HTTPException(
                status_code=400,
                detail="Device limit reached.",
            )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_device(
        db,
        customer_id,
        mac_address,
        device_name=None,
        approved_by_customer=True,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id == customer_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        existing_device = (
            DeviceService._find_device_by_mac(
                db,
                mac_address,
            )
        )

        if existing_device:

            raise HTTPException(
                status_code=400,
                detail="Device already exists.",
            )

        subscription = (
            DeviceService._get_active_subscription(
                db,
                customer_id,
            )
        )

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id == subscription.plan_id
            )
            .first()
        )

        DeviceService._validate_device_limit(
            db,
            customer_id,
            plan,
        )

        device = Device(
            customer_id=customer_id,
            device_name=device_name,
            mac_address=mac_address,
            approved_by_customer=approved_by_customer,
            device_status=DeviceStatus.ACTIVE,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow(),
        )

        db.add(device)

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def activate_device(
        db,
        device_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        if device.device_status == DeviceStatus.BLOCKED:

            raise HTTPException(
                status_code=400,
                detail="Blocked devices cannot be activated.",
            )

        subscription = (
            DeviceService._get_active_subscription(
                db,
                device.customer_id,
            )
        )

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id == subscription.plan_id
            )
            .first()
        )

        DeviceService._validate_device_limit(
            db,
            device.customer_id,
            plan,
        )

        device.device_status = DeviceStatus.ACTIVE
        device.last_seen = datetime.utcnow()

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def deactivate_device(
        db,
        device_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        device.device_status = DeviceStatus.INACTIVE

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def replace_device(
        db,
        customer_id,
        old_device_id,
        new_device_id,
    ):

        old_device = (
            DeviceService._find_device(
                db,
                old_device_id,
            )
        )

        new_device = (
            DeviceService._find_device(
                db,
                new_device_id,
            )
        )

        if (
            old_device.customer_id != customer_id
            or
            new_device.customer_id != customer_id
        ):

            raise HTTPException(
                status_code=400,
                detail="Device does not belong to this customer.",
            )

        old_device.device_status = (
            DeviceStatus.INACTIVE
        )

        new_device.device_status = (
            DeviceStatus.ACTIVE
        )

        new_device.last_seen = (
            datetime.utcnow()
        )

        db.commit()

        db.refresh(new_device)

        return new_device

    @staticmethod
    def approve_device(
        db,
        device_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        device.approved_by_customer = True

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def rename_device(
        db,
        device_id,
        device_name,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        device.device_name = device_name

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def block_device(
        db,
        device_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        device.device_status = DeviceStatus.BLOCKED

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def update_last_seen(
        db,
        mac_address,
    ):

        device = (
            DeviceService._find_device_by_mac(
                db,
                mac_address,
            )
        )

        if not device:

            return None

        device.last_seen = datetime.utcnow()

        db.commit()

        db.refresh(device)

        return device

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_device(
        db,
        device_id,
    ):

        return (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

    @staticmethod
    def get_customer_devices(
        db,
        customer_id,
    ):

        return (
            db.query(Device)
            .filter(
                Device.customer_id == customer_id,
            )
            .order_by(
                Device.device_name
            )
            .all()
        )

    @staticmethod
    def get_active_devices(
        db,
        customer_id,
    ):

        return (
            db.query(Device)
            .filter(
                Device.customer_id == customer_id,
                Device.device_status == DeviceStatus.ACTIVE,
            )
            .order_by(
                Device.device_name
            )
            .all()
        )

    @staticmethod
    def get_all_devices(
        db,
    ):

        return (
            db.query(Device)
            .order_by(
                Device.customer_id,
                Device.device_name,
            )
            .all()
        )