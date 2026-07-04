from fastapi import HTTPException

from typing import cast

from app.enums.customer_status import CustomerStatus
from app.enums.next_action import NextAction

from app.models.customer import Customer

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    REGISTER_CUSTOMER,
    START_ONBOARDING,
    COMPLETE_ONBOARDING,
    UPDATE_CUSTOMER,
    ACTIVATE_CUSTOMER,
    DEACTIVATE_CUSTOMER,
)

from app.enums.audit_result import AuditResult

class CustomerService:

    @staticmethod
    def register_customer(
        db,
        phone_number,
        full_name,
    ):

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        customer = Customer(
            phone_number=phone_number,
            full_name=full_name,
            telegram_user_id=None,
            status=CustomerStatus.ACTIVE,
            is_registered=True,
            registration_step=NextAction.COMPLETE,
        )

        db.add(customer)

        # Generate the primary key before logging
        db.flush()

        customer_id = cast(int, customer.customer_id)
        customer_name = cast(str,customer.full_name)

        AuditLogService.log_system_action(

            db=db,

            action=REGISTER_CUSTOMER,

            entity_type="Customer",

            target_name=customer_name,

            entity_id=customer_id,

            result=AuditResult.SUCCESS,

            description=(
                "Customer registered by administrator."
            ),

            new_values={
                "phone_number": customer.phone_number,
                "status": customer.status.value,
            },

        )

        db.commit()

        db.refresh(customer)

        return customer

    @staticmethod
    def start_onboarding(
        db,
        telegram_user_id,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if customer:
            return customer

        customer = Customer(
            telegram_user_id=telegram_user_id,
            is_registered=False,
            registration_step=NextAction.START_ONBOARDING,
        )

        db.add(customer)
        
        AuditLogService.log_system_action(

            db=db,

            action=START_ONBOARDING,

            entity_type="Customer",

            target_name=str(telegram_user_id),

            result=AuditResult.SUCCESS,

            description=(
                "Customer started Telegram onboarding."
            ),

            new_values={
                "telegram_user_id": telegram_user_id,
            },

        )        
        
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def update_full_name(
        db,
        telegram_user_id,
        full_name,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.full_name = full_name

        customer.registration_step = (
            NextAction.ENTER_PHONE_NUMBER
        )

        db.commit()

        db.refresh(
            customer,
        )

        return customer

    @staticmethod
    def update_phone_number(
        db,
        telegram_user_id,
        phone_number,
    ):

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number,
                Customer.telegram_user_id != telegram_user_id,
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:

            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        customer.phone_number = phone_number

        customer.status = CustomerStatus.ACTIVE

        customer.is_registered = True

        customer.registration_step = (
            NextAction.COMPLETE
        )

        AuditLogService.log_system_action(

            db=db,

            action=COMPLETE_ONBOARDING,

            entity_type="Customer",

            target_name=customer.full_name,

            entity_id=customer.customer_id,

            result=AuditResult.SUCCESS,

            description=(
                "Customer completed Telegram onboarding."
            ),

            new_values={
                "phone_number": customer.phone_number,
                "status": customer.status.value,
            },

        )

        db.commit()

        db.refresh(
            customer,
        )

        return customer

    @staticmethod
    def update_customer(
        db,
        customer_id,
        customer_data,
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

        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == customer_data.phone_number,
                Customer.customer_id != customer_id,
            )
            .first()
        )

        if existing_customer:
            raise HTTPException(
                status_code=400,
                detail="Customer with this phone number already exists.",
            )

        old_values = {
            "full_name": customer.full_name,
            "phone_number": customer.phone_number,
        }

        customer.full_name = customer_data.full_name
        customer.phone_number = customer_data.phone_number

        AuditLogService.log_system_action(

            db=db,

            action=UPDATE_CUSTOMER,

            entity_type="Customer",

            target_name=str(customer.full_name),

            entity_id=int(customer.customer_id),

            result=AuditResult.SUCCESS,

            description=(
                "Customer details updated."
            ),

            old_values=old_values,

            new_values={
                "full_name": customer.full_name,
                "phone_number": customer.phone_number,
            },

        )

        db.commit()

        db.refresh(customer)

        return customer

    @staticmethod
    def activate_customer(
        db,
        customer_id,
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

        customer.status = CustomerStatus.ACTIVE

        AuditLogService.log_system_action(

            db=db,

            action=ACTIVATE_CUSTOMER,

            entity_type="Customer",

            target_name=customer.full_name,

            entity_id=customer.customer_id,

            result=AuditResult.SUCCESS,

            description=(
                "Customer activated."
            ),

        )

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def deactivate_customer(
        db,
        customer_id,
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

        customer.status = CustomerStatus.SUSPENDED

        AuditLogService.log_system_action(

            db=db,

            action=DEACTIVATE_CUSTOMER,

            entity_type="Customer",

            target_name=customer.full_name,

            entity_id=customer.customer_id,

            result=AuditResult.SUCCESS,

            description=(
                "Customer suspended."
            ),

        )

        db.commit()
        
        db.refresh(customer)

        return customer

    @staticmethod
    def get_customer(
        db,
        customer_id,
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

        return customer

    @staticmethod
    def get_customer_by_phone(
        db,
        phone_number,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.phone_number == phone_number
            )
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        return customer

    @staticmethod
    def get_customer_by_telegram_id(
        db,
        telegram_user_id,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.telegram_user_id == telegram_user_id
            )
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found.",
            )

        return customer

    @staticmethod
    def _apply_sort(
        query,
        sort_column,
        sort_order,
    ):

        if sort_order.lower() == "desc":

            return query.order_by(
                sort_column.desc(),
            )

        return query.order_by(
            sort_column.asc(),
        )

    @staticmethod
    def get_all_customers(
        db,
        page=1,
        page_size=25,
        search=None,
        sort_by="customer_id",
        sort_order="asc",
    ):

        query = (
            db.query(
                Customer,
            )
        )

        if search:

            query = query.filter(

                Customer.full_name.ilike(
                    f"%{search}%"
                )

                |

                Customer.phone_number.ilike(
                    f"%{search}%"
                )

            )

        total = query.count()

        sort_column = {

            "customer_id":
                Customer.customer_id,

            "full_name":
                Customer.full_name,

            "phone_number":
                Customer.phone_number,

        }.get(

            sort_by,

            Customer.customer_id,

        )

        query = (
            CustomerService._apply_sort(
                query,
                sort_column,
                sort_order,
            )
        )

        customers = (

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

            "items": customers,

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": pages,

        }