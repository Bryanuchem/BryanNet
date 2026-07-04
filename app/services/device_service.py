from datetime import datetime, UTC

from fastapi import HTTPException

from app.enums import DeviceStatus

from app.enums import SubscriptionStatus

from app.models.subscription import Subscription

from app.models.device import Device

from app.services.customer_service import CustomerService

from sqlalchemy.orm import Session

from typing import cast

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    REGISTER_DEVICE,
    APPROVE_DEVICE,
    BLOCK_DEVICE,
    UNBLOCK_DEVICE,
    RENAME_DEVICE,
    REPLACE_DEVICE,
    ACTIVATE_DEVICE,
    DEACTIVATE_DEVICE,
)

from app.enums.audit_result import AuditResult

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

            db.query(Subscription)

            .filter(

                Subscription.customer_id
                == customer_id,

                Subscription.status
                == SubscriptionStatus.ACTIVE,

            )

            .first()

        )

        if not subscription:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Customer has no active "
                    "subscription."
                ),
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

    @staticmethod
    def _finalize_device_change(
        db,
        device,
        synchronize=True,
    ):

        db.commit()

        db.refresh(
            device,
        )

        if synchronize:

            from app.services.router_account_service import (
                RouterAccountService,
            )

            RouterAccountService.synchronize_customer_access(

                db,

                device.customer_id,

            )

        return device
    
    @staticmethod
    def _apply_sort(
        query,
        *sort_columns,
        sort_order,
    ):

        columns = [
            column.desc() if sort_order.lower() == "desc" else column.asc()
            for column in sort_columns
        ]

        return query.order_by(*columns)
   
    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_device(
        db,
        customer_id,
        mac_address,
        admin_id,
        device_name=None,
        approved_by_customer=True,
    ):

        CustomerService.get_customer(
            db,
            customer_id,
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

        from app.services.plan_service import PlanService

        plan = (
            PlanService.get_plan(
                db,
                subscription.plan_id,
            )
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

            first_seen=datetime.now(UTC),

            last_seen=datetime.now(UTC),

        )

        db.add(
            device,
        )

        db.flush()

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=REGISTER_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Registered device '{device.device_name or device.mac_address}'."
            ),

            new_values={
                "customer_id": cast(int, device.customer_id),
                "mac_address": cast(str, device.mac_address),
                "device_status": device.device_status.value,
                "approved_by_customer": cast(
                    bool,
                    device.approved_by_customer,
                ),
            },

        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
            )
        )

    @staticmethod
    def activate_device(
        db,
        device_id,
        admin_id,
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

        from app.services.plan_service import PlanService

        plan = (
            PlanService.get_plan(
                db,
                subscription.plan_id,
            )
        )

        DeviceService._validate_device_limit(
            db,
            device.customer_id,
            plan,
        )

        old_status = device.device_status.value

        device.device_status = (
            DeviceStatus.ACTIVE
        )

        device.last_seen = (
            datetime.now(UTC)
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=ACTIVATE_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Activated device '{device.device_name or device.mac_address}'."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService
            ._finalize_device_change(
                db,
                device,
            )
        )

    @staticmethod
    def deactivate_device(
        db,
        device_id,
        admin_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        old_status = device.device_status.value

        device.device_status = (
            DeviceStatus.INACTIVE
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=DEACTIVATE_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Deactivated device '{device.device_name or device.mac_address}'."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService
            ._finalize_device_change(
                db,
                device,
            )
        )

    @staticmethod
    def replace_device(
        db,
        customer_id,
        old_device_id,
        new_device_id,
        admin_id,
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

        old_status = old_device.device_status

        old_device.device_status = (
            DeviceStatus.INACTIVE
        )

        new_device.device_status = (
            DeviceStatus.ACTIVE
        )

        new_device.last_seen = (
            datetime.now(UTC)
        )

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=REPLACE_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                new_device.device_id,
            ),

            target_name=(
                new_device.device_name
                or new_device.mac_address
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Replaced device "
                f"'{old_device.device_name or old_device.mac_address}' "
                f"with "
                f"'{new_device.device_name or new_device.mac_address}'."
            ),

            old_values={
                "old_device_id": old_device.device_id,
                "old_device_name": old_device.device_name,
                "old_status": old_status.value,
            },

            new_values={
                "new_device_id": new_device.device_id,
                "new_device_name": new_device.device_name,
                "new_status": DeviceStatus.ACTIVE.value,
            },

        )

        return (
            DeviceService._finalize_device_change(
                db,
                new_device,
            )
        )
    
    @staticmethod
    def approve_device(
        db,
        device_id,
        admin_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        old_value = device.approved_by_customer

        device.approved_by_customer = True

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=APPROVE_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Approved device '{device.device_name or device.mac_address}'."
            ),

            old_values={
                "approved_by_customer": old_value,
            },

            new_values={
                "approved_by_customer": True,
            },

        )

        return (
            DeviceService
            ._finalize_device_change(
                db,
                device,
            )
        )

    @staticmethod
    def rename_device(
        db: Session,
        device_id: int,
        device_name: str,
        admin_id: int,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        old_name = device.device_name

        device.device_name = device_name

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=RENAME_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=device_name,

            result=AuditResult.SUCCESS,

            description=(
                f"Renamed device from "
                f"'{old_name}' to '{device_name}'."
            ),

            old_values={
                "device_name": old_name,
            },

            new_values={
                "device_name": device_name,
            },

        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
                synchronize=False,
            )
        )

    @staticmethod
    def block_device(
        db: Session,
        device_id: int,
        admin_id: int,
    ):

        device = (
            DeviceService.get_device(
                db=db,
                device_id=device_id,
            )
        )

        if device.device_status == DeviceStatus.BLOCKED:

            raise HTTPException(
                status_code=400,
                detail="Device is already blocked.",
            )

        old_status = device.device_status

        device.device_status = DeviceStatus.BLOCKED

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=BLOCK_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Blocked device '{device.device_name or device.mac_address}'."
            ),

            old_values={
                "device_status": old_status.value,
            },

            new_values={
                "device_status": DeviceStatus.BLOCKED.value,
            },

        )

        return (
            DeviceService._finalize_device_change(
                db=db,
                device=device,
            )
        )

    @staticmethod
    def unblock_device(
        db: Session,
        device_id: int,
        admin_id: int,
    ):

        device = (
            DeviceService.get_device(
                db=db,
                device_id=device_id,
            )
        )

        if device.device_status != DeviceStatus.BLOCKED:

            raise HTTPException(
                status_code=400,
                detail="Device is not blocked.",
            )

        old_status = device.device_status

        device.device_status = DeviceStatus.INACTIVE

        AuditLogService.log_admin_action(

            db=db,

            admin_id=cast(
                int,
                admin_id,
            ),

            action=UNBLOCK_DEVICE,

            entity_type="Device",

            entity_id=cast(
                int,
                device.device_id,
            ),

            target_name=cast(
                str,
                device.device_name or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Unblocked device '{device.device_name or device.mac_address}'."
            ),

            old_values={
                "device_status": old_status.value,
            },

            new_values={
                "device_status": DeviceStatus.INACTIVE.value,
            },

        )

        return (
            DeviceService._finalize_device_change(
                db=db,
                device=device,
            )
        )

    @staticmethod
    def touch_device(
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

        device.last_seen = (
            datetime.now(UTC)
        )

        return (
            DeviceService
            ._finalize_device_change(
                db,
                device,
                synchronize=False,
            )
        )

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
                Device.device_name,
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
                Device.device_name,
            )
            .all()
        )

    @staticmethod
    def get_all_devices(
        db,
        page=1,
        page_size=25,
        search=None,
        customer_id=None,
        device_status=None,
        sort_by="device_id",
        sort_order="asc",
    ):

        query = (
            db.query(Device)
        )

        if search:

            query = query.filter(

                Device.device_name.ilike(
                    f"%{search}%"
                )

                |

                Device.mac_address.ilike(
                    f"%{search}%"
                )

            )

        if customer_id is not None:

            query = query.filter(
                Device.customer_id == customer_id,
            )

        if device_status is not None:

            query = query.filter(
                Device.device_status == device_status,
            )

        total = query.count()

        sort_column = {

            "device_id":
                Device.device_id,

            "device_name":
                Device.device_name,

            "last_seen":
                Device.last_seen,

        }.get(

            sort_by,

            Device.device_id,

        )

        query = DeviceService._apply_sort(
            query,
            Device.customer_id,
            sort_column,
            sort_order=sort_order,
        )

        devices = (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )

        pages = (

            (total + page_size - 1)

            // page_size

            if total

            else 0

        )

        return {

            "items": devices,

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": pages,

        }