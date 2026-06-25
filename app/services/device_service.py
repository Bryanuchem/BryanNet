from app.models.device import Device
from app.models.plan import Plan
from fastapi import HTTPException

from app.services.subscription_service import (
    SubscriptionService
)


class DeviceService:

    @staticmethod
    def register_device(
        db,
        customer_id,
        device_name,
        mac_address
    ):

        active_subscription = (
            SubscriptionService
            .get_active_subscription(
                db,
                customer_id
            )
        )

        if not active_subscription:
            raise HTTPException(
                status_code=400,
                detail="No active subscription found"
            )

        plan = (
            db.query(Plan)
            .filter(
                Plan.plan_id ==
                active_subscription.plan_id
            )
            .first()
        )

        active_devices = (
            db.query(Device)
            .filter(
                Device.customer_id == customer_id,
                Device.device_status == "active"
            )
            .count()
        )

        if active_devices >= plan.max_devices:
            raise HTTPException(
                status_code=400,
                detail="Device limit reached"
            )

        device = Device(
            customer_id=customer_id,
            device_name=device_name,
            mac_address=mac_address
        )

        db.add(device)

        db.commit()

        db.refresh(device)

        return device

    @staticmethod
    def get_customer_devices(
        db,
        customer_id
    ):

        return (
            db.query(Device)
            .filter(
                Device.customer_id == customer_id,
                Device.device_status == "active"
            )
            .all()
        )
        
    @staticmethod
    def remove_device(
        db,
        device_id
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
                detail="Device not found"
            )

        device.device_status = "removed"

        db.commit()

        db.refresh(device)

        return {
            "message": "Device removed successfully"
        }        