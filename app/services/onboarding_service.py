from fastapi import HTTPException

from app.constants.audit_actions import (
    COMPLETE_ONBOARDING,
    START_ONBOARDING,
)

from app.enums.audit_result import (
    AuditResult,
)

from app.enums.customer_status import (
    CustomerStatus,
)

from app.enums.next_action import (
    NextAction,
)

from app.models.customer import (
    Customer,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.utils.phone import (
    normalize_nigerian_phone_number,
)


class OnboardingService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_customer(
        db,
        telegram_user_id,
    ):

        customer = (

            db.query(Customer)

            .filter(
                Customer.telegram_user_id
                == telegram_user_id,
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
        telegram_user_id,
    ):

        phone_number = (
            normalize_nigerian_phone_number(
                phone_number,
            )
        )

        existing_customer = (

            db.query(Customer)

            .filter(
                Customer.phone_number
                == phone_number,

                Customer.telegram_user_id
                != telegram_user_id,
            )

            .first()

        )

        if existing_customer:

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
        telegram_user_id,
    ):

        existing_customer = (

            db.query(Customer)

            .filter(
                Customer.email == email,

                Customer.telegram_user_id
                != telegram_user_id,
            )

            .first()

        )

        if existing_customer:

            raise HTTPException(

                status_code=400,

                detail=(
                    "Customer with this email "
                    "already exists."
                ),

            )

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def start_onboarding(
        db,
        telegram_user_id,
    ):

        customer = (

            db.query(Customer)

            .filter(
                Customer.telegram_user_id
                == telegram_user_id,
            )

            .first()

        )

        if customer:

            return customer

        customer = Customer(

            telegram_user_id=telegram_user_id,

            is_registered=False,

            registration_step=(
                NextAction.ENTER_NAME
            ),

        )

        db.add(customer)

        AuditLogService.log_system_action(

            db=db,

            action=START_ONBOARDING,

            entity_type="Customer",

            target_name=str(
                telegram_user_id,
            ),

            result=AuditResult.SUCCESS,

            description=(
                "Customer started "
                "Telegram onboarding."
            ),

            new_values={
                "telegram_user_id":
                    telegram_user_id,
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
            OnboardingService
            ._get_customer(
                db,
                telegram_user_id,
            )
        )

        customer.full_name = full_name

        customer.registration_step = (
            NextAction.ENTER_PHONE_NUMBER
        )

        db.commit()

        db.refresh(customer)

        return customer

    @staticmethod
    def update_phone_number(
        db,
        telegram_user_id,
        phone_number,
    ):

        customer = (
            OnboardingService
            ._get_customer(
                db,
                telegram_user_id,
            )
        )

        customer.phone_number = (

            OnboardingService
            ._validate_phone_available(
                db,
                phone_number,
                telegram_user_id,
            )

        )

        customer.registration_step = (
            NextAction.ENTER_EMAIL
        )

        db.commit()

        db.refresh(customer)

        return customer

    @staticmethod
    def update_email(
        db,
        telegram_user_id,
        email,
    ):

        customer = (
            OnboardingService
            ._get_customer(
                db,
                telegram_user_id,
            )
        )

        OnboardingService._validate_email_available(
            db,
            email,
            telegram_user_id,
        )

        customer.email = email

        customer.status = (
            CustomerStatus.ACTIVE
        )

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
                "Customer completed "
                "Telegram onboarding."
            ),

            new_values={
                "phone_number":
                    customer.phone_number,
                "email":
                    customer.email,
                "status":
                    customer.status.value,
            },

        )

        db.commit()

        db.refresh(customer)

        return customer