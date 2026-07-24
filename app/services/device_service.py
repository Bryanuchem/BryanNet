from datetime import datetime, UTC

from fastapi import HTTPException

from app.enums import DeviceStatus

from app.enums import SubscriptionStatus

from app.models.subscription import Subscription

from app.models.device import Device

from app.models.customer import Customer

from app.schemas.device import (
    DeviceListItem,
    DeviceResponse,
)

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

            from app.services.router_provisioning_service import (
                RouterProvisioningService,
            )

            RouterProvisioningService.synchronize_customer_access(

                db,

                device.customer_id,

            )

        return device
    
    @staticmethod
    def _find_by_mac_address(
        db,
        mac_address,
    ):

        return (

            db.query(
                Device,
            )

            .filter(

                Device.mac_address
                == mac_address,

            )

            .first()

        )
    
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

    @staticmethod
    def _build_device_response(
        db,
        device,
    ):

        customer = CustomerService.get_customer(
            db,
            device.customer_id,
        )

        return DeviceResponse(

            device_id=device.device_id,

            customer_id=device.customer_id,

            customer_name=customer.full_name,

            device_name=device.device_name,

            mac_address=device.mac_address,

            device_status=device.device_status,
            
            online=device.online,

        )
        
    @staticmethod
    def _set_device_active(
        db,
        device,
    ):

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

        from app.services.plan_service import (
            PlanService,
        )

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

        device.device_status = (
            DeviceStatus.ACTIVE
        )

        device.last_seen = (
            datetime.now(UTC)
        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
            )
        )


    @staticmethod
    def _set_device_inactive(
        db,
        device,
    ):

        device.device_status = (
            DeviceStatus.INACTIVE
        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
            )
        )


    @staticmethod
    def _set_device_blocked(
        db,
        device,
    ):

        if device.device_status == DeviceStatus.BLOCKED:

            raise HTTPException(
                status_code=400,
                detail="Device is already blocked.",
            )

        device.device_status = (
            DeviceStatus.BLOCKED
        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
            )
        )


    @staticmethod
    def _set_device_unblocked(
        db,
        device,
    ):

        if device.device_status != DeviceStatus.BLOCKED:

            raise HTTPException(
                status_code=400,
                detail="Device is not blocked.",
            )

        device.device_status = (
            DeviceStatus.INACTIVE
        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
            )
        )
         
    @staticmethod
    def _set_device_name(
        db,
        device,
        device_name,
    ):

        device.device_name = (
            device_name
        )

        return (
            DeviceService._finalize_device_change(
                db,
                device,
                synchronize=False,
            )
        )
 
    @staticmethod
    def _set_online(
        device,
    ):

        device.online = True

        device.last_seen = (
            datetime.now(UTC)
        )

        return device

    @staticmethod
    def _set_offline(
        device,
    ):

        device.online = False

        return device

    @staticmethod
    def _set_online_no_commit(
        device,
    ):

        DeviceService._set_online(
            device,
        )

        return device
               
    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_device(
        db,
        customer_id,
        mac_address,
        admin_id=None,
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
            
            online=False,

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
                f"Device '{device.device_name or device.mac_address}' was registered."
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

        device = DeviceService._finalize_device_change(
            db,
            device,
        )

        return DeviceService._build_device_response(
            db,
            device,
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

        old_status = (
            device.device_status.value
        )

        device = (
            DeviceService._set_device_active(
                db,
                device,
            )
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
                device.device_name
                or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Device '{device.device_name or device.mac_address}' "
                f"was activated."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService._build_device_response(
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

        old_status = (
            device.device_status.value
        )

        device = (
            DeviceService._set_device_inactive(
                db,
                device,
            )
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
                device.device_name
                or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Device '{device.device_name or device.mac_address}' "
                f"was deactivated."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService._build_device_response(
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
                f"Device "
                f"'{old_device.device_name or old_device.mac_address}' "
                f"was replaced with "
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

        new_device = DeviceService._finalize_device_change(
            db,
            new_device,
        )

        return DeviceService._build_device_response(
            db,
            new_device,
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
                f"Device '{device.device_name or device.mac_address}' was approved."
            ),

            old_values={
                "approved_by_customer": old_value,
            },

            new_values={
                "approved_by_customer": True,
            },

        )

        device = DeviceService._finalize_device_change(
            db,
            device,
        )

        return DeviceService._build_device_response(
            db,
            device,
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

        old_name = (
            device.device_name
        )

        device = (
            DeviceService._set_device_name(
                db,
                device,
                device_name,
            )
        )

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

            target_name=cast(
                str,
                device.device_name
                or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Device '{device.mac_address}' "
                f"was renamed to "
                f"'{device.device_name}'."
            ),

            old_values={
                "device_name": old_name,
            },

            new_values={
                "device_name": device.device_name,
            },

        )

        return (
            DeviceService._build_device_response(
                db,
                device,
            )
        )

    @staticmethod
    def block_device(
        db: Session,
        device_id: int,
        admin_id: int,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        old_status = (
            device.device_status.value
        )

        device = (
            DeviceService._set_device_blocked(
                db,
                device,
            )
        )

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
                device.device_name
                or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Device '{device.device_name or device.mac_address}' "
                f"was blocked."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService._build_device_response(
                db,
                device,
            )
        )

    @staticmethod
    def unblock_device(
        db: Session,
        device_id: int,
        admin_id: int,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        old_status = (
            device.device_status.value
        )

        device = (
            DeviceService._set_device_unblocked(
                db,
                device,
            )
        )

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
                device.device_name
                or device.mac_address,
            ),

            result=AuditResult.SUCCESS,

            description=(
                f"Device '{device.device_name or device.mac_address}' "
                f"was unblocked."
            ),

            old_values={
                "device_status": old_status,
            },

            new_values={
                "device_status": device.device_status.value,
            },

        )

        return (
            DeviceService._build_device_response(
                db,
                device,
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

    @staticmethod
    def set_online(
        db,
        mac_address,
    ):

        device = (

            DeviceService

            ._find_device_by_mac(

                db,

                mac_address,

            )

        )

        if not device:

            return None

        DeviceService._set_online(
            device,
        )

        db.commit()

        db.refresh(
            device,
        )

        return device


    @staticmethod
    def set_offline(
        db,
        mac_address,
    ):

        device = (

            DeviceService

            ._find_device_by_mac(

                db,

                mac_address,

            )

        )

        if not device:

            return None

        DeviceService._set_offline(
            device,
        )

        db.commit()

        db.refresh(
            device,
        )

        return device
        
    # ==========================================================
    # Query Methods
    # ==========================================================
    
    @staticmethod
    def find_by_mac_address(
        db,
        mac_address,
    ):

        return (

            DeviceService

            ._find_by_mac_address(

                db,

                mac_address,

            )

        )

    @staticmethod
    def count_online_devices(
        db,
        customer_id,
    ):

        return (

            db.query(

                Device,

            )

            .filter(

                Device.customer_id
                == customer_id,

                Device.online.is_(True),

            )

            .count()

        )

    @staticmethod
    def count_registered_devices(
        db,
        customer_id,
    ):

        return (

            db.query(

                Device,

            )

            .filter(

                Device.customer_id
                == customer_id,

                Device.device_status
                != DeviceStatus.BLOCKED,

            )

            .count()

        )
        
    @staticmethod
    def get_device(
        db,
        device_id,
    ):

        device = (
            DeviceService._find_device(
                db,
                device_id,
            )
        )

        return (
            DeviceService._build_device_response(
                db,
                device,
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

            db.query(

                Device,

                Customer.full_name.label(
                    "customer_name",
                ),

            )

            .join(

                Customer,

                Customer.customer_id
                == Device.customer_id,

            )

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

        results = (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )

        devices = [

            DeviceListItem(

                device_id=device.device_id,

                customer_id=device.customer_id,

                customer_name=customer_name,

                device_name=device.device_name,

                mac_address=device.mac_address,

                device_status=device.device_status,

                online=device.online,
                
                approved_by_customer=device.approved_by_customer,

                first_seen=device.first_seen,

                last_seen=device.last_seen,

            )

            for device, customer_name in results

        ]

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