from sqlalchemy.orm import (
    Session,
)

from app.schemas.portal_onboarding import (
    PortalOnboardingResponse,
    PortalOnboardingStart,
    PortalUpdateName,
    PortalUpdatePhone,
)

from app.services.customer_service import (
    CustomerService,
)


class PortalOnboardingService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _build_response(
        customer,
    ):

        return PortalOnboardingResponse(

            customer_id=customer.customer_id,

            telegram_user_id=(
                customer.telegram_user_id
            ),

            full_name=(
                customer.full_name
            ),

            phone_number=(
                customer.phone_number
            ),

            is_registered=(
                customer.is_registered
            ),

            status=(
                customer.status.value
            ),

            registration_step=(
                customer.registration_step.value
            ),

        )

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def start_onboarding(
        db: Session,
        request: PortalOnboardingStart,
    ):

        customer = (
            CustomerService.start_onboarding(
                db=db,
                telegram_user_id=(
                    request.telegram_user_id
                ),
            )
        )

        return (
            PortalOnboardingService
            ._build_response(
                customer,
            )
        )

    @staticmethod
    def update_full_name(
        db: Session,
        request: PortalUpdateName,
    ):

        customer = (
            CustomerService.update_full_name(
                db=db,
                telegram_user_id=(
                    request.telegram_user_id
                ),
                full_name=(
                    request.full_name
                ),
            )
        )

        return (
            PortalOnboardingService
            ._build_response(
                customer,
            )
        )

    @staticmethod
    def update_phone_number(
        db: Session,
        request: PortalUpdatePhone,
    ):

        customer = (
            CustomerService.update_phone_number(
                db=db,
                telegram_user_id=(
                    request.telegram_user_id
                ),
                phone_number=(
                    request.phone_number
                ),
            )
        )

        return (
            PortalOnboardingService
            ._build_response(
                customer,
            )
        )