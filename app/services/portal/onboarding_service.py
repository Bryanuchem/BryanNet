from sqlalchemy.orm import (
    Session,
)

from app.schemas.portal_onboarding import (
    PortalOnboardingResponse,
    PortalOnboardingStart,
    PortalUpdateName,
    PortalUpdatePhone,
    PortalUpdateEmail,
)

from app.services.onboarding_service import (
    OnboardingService,
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

            email=(
                customer.email
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
            OnboardingService.start_onboarding(
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
            OnboardingService.update_full_name(
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
            OnboardingService.update_phone_number(
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
        
    @staticmethod
    def update_email(
        db: Session,
        request: PortalUpdateEmail,
    ):

        customer = (
            OnboardingService
            .update_email(
                db=db,
                telegram_user_id=(
                    request.telegram_user_id
                ),
                email=(
                    request.email
                ),
            )
        )

        return (
            PortalOnboardingService
            ._build_response(
                customer,
            )
        )