from fastapi import HTTPException

from typing import cast

from app.enums.customer_status import CustomerStatus
from app.enums.next_action import NextAction

from app.models.customer import Customer

from app.services.audit_log_service import AuditLogService

from app.constants.audit_actions import (
    REGISTER_CUSTOMER,
    UPDATE_CUSTOMER,
    ACTIVATE_CUSTOMER,
    DEACTIVATE_CUSTOMER,
)

from app.utils.phone import (
    normalize_nigerian_phone_number,
)

from app.enums.audit_result import AuditResult

class CustomerService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_customer(
        db,
        customer_id,
    ):

        customer = (

            db.query(Customer)

            .filter(
                Customer.customer_id == customer_id,
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
    def _validate_phone_available(
        db,
        phone_number,
        customer_id=None,
    ):

        phone_number = (
            normalize_nigerian_phone_number(
                phone_number,
            )
        )

        query = (

            db.query(Customer)

            .filter(
                Customer.phone_number == phone_number,
            )

        )

        if customer_id is not None:

            query = query.filter(
                Customer.customer_id != customer_id,
            )

        if query.first():

            raise HTTPException(

                status_code=400,

                detail=(
                    "Customer with this phone "
                    "number already exists."
                ),

            )

        return phone_number


    @staticmethod
    def _validate_email_available(
        db,
        email,
        customer_id=None,
    ):

        query = (

            db.query(Customer)

            .filter(
                Customer.email == email,
            )

        )

        if customer_id is not None:

            query = query.filter(
                Customer.customer_id != customer_id,
            )

        if query.first():

            raise HTTPException(

                status_code=400,

                detail=(
                    "Customer with this email "
                    "already exists."
                ),

            )

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

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_customer(
        db,
        phone_number,
        full_name,
        email,
    ):

        phone_number = (
            CustomerService
            ._validate_phone_available(
                db,
                phone_number,
            )
        )

        CustomerService._validate_email_available(
            db,
            email,
        )

        customer = Customer(
            phone_number=phone_number,
            full_name=full_name,
            email=email,
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

                f"Customer "

                f"'{customer.full_name}' "

                f"was registered."

            ),

            new_values={
                "phone_number": customer.phone_number,
                "email": customer.email,
                "status": customer.status.value,
            },

        )

        db.commit()

        db.refresh(customer)

        return customer

    @staticmethod
    def update_customer(
        db,
        customer_id,
        customer_data,
    ):


        customer = (
            CustomerService._find_customer(
                db,
                customer_id,
            )
        )

        customer_data.phone_number = (

            CustomerService
            ._validate_phone_available(

                db,

                customer_data.phone_number,

                customer_id,

            )

        )

        CustomerService._validate_email_available(

            db,

            customer_data.email,

            customer_id,

        )

        old_values = {
            "full_name": customer.full_name,
            "phone_number": customer.phone_number,
            "email": customer.email,
        }

        customer.full_name = customer_data.full_name
        customer.phone_number = customer_data.phone_number
        customer.email = customer_data.email

        AuditLogService.log_system_action(

            db=db,

            action=UPDATE_CUSTOMER,

            entity_type="Customer",

            target_name=str(customer.full_name),

            entity_id=int(customer.customer_id),

            result=AuditResult.SUCCESS,

            description=(

                f"Customer "

                f"'{customer.full_name}' "

                f"details were updated."

            ),

            old_values=old_values,

            new_values={
                "full_name": customer.full_name,
                "phone_number": customer.phone_number,
                "email": customer.email,
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
            CustomerService._find_customer(
                db,
                customer_id,
            )
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

                f"Customer "

                f"'{customer.full_name}' "

                f"was activated."

            ),

            old_values={

                "status": CustomerStatus.SUSPENDED.value,

            },

            new_values={

                "status": CustomerStatus.ACTIVE.value,

            },

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
            CustomerService._find_customer(
                db,
                customer_id,
            )
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

                f"Customer "

                f"'{customer.full_name}' "

                f"was suspended."

            ),
            
            old_values={

                "status": CustomerStatus.ACTIVE.value,

            },

            new_values={

                "status": CustomerStatus.SUSPENDED.value,

            },
        )

        db.commit()
        
        db.refresh(customer)

        return customer

    @staticmethod
    def get_customer(
        db,
        customer_id,
    ):

        return (
            CustomerService._find_customer(
                db,
                customer_id,
            )
        )

    @staticmethod
    def get_customer_by_phone(
        db,
        phone_number,
    ):
        phone_number = normalize_nigerian_phone_number(
            phone_number,
        )

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
    def get_customer_by_email(
        db,
        email,
    ):

        customer = (
            db.query(Customer)
            .filter(
                Customer.email == email,
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

                |

                Customer.email.ilike(
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

            "email":
                Customer.email,

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