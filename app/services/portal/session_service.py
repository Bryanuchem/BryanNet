from sqlalchemy.orm import (
    Session,
)

from app.schemas.portal_session import (
    PortalSessionRegister,
    PortalSessionResponse,
)

from app.services.session_service import (
    SessionService,
)


class PortalSessionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _build_session_response(
        session,
        telegram_user_id: int,
    ):

        customer = session.get(
            "customer",
        )

        return PortalSessionResponse(

            is_registered=(
                customer is not None
                and
                customer.registration_step.value
                == "complete"
            ),

            customer_id=(
                customer.customer_id
                if customer
                else None
            ),

            full_name=(
                customer.full_name
                if customer
                else None
            ),

            telegram_user_id=telegram_user_id,

            has_active_subscription=session[
                "has_active_subscription"
            ],

            next_action=session[
                "next_action"
            ],

        )

    # ==========================================================
    # Public Methods
    # ==========================================================
    
    @staticmethod
    def get_session(
        db: Session,
        telegram_user_id: int,
        first_login: bool = False,
    ):

        session = (
            SessionService.get_session(
                db=db,
                telegram_user_id=telegram_user_id,
                first_login=first_login,
            )
        )

        return (
            PortalSessionService
            ._build_session_response(
                session,
                telegram_user_id,
            )
        )

    @staticmethod
    def refresh_session(
        db: Session,
        telegram_user_id: int,
    ):

        return (
            PortalSessionService.get_session(
                db=db,
                telegram_user_id=telegram_user_id,
                first_login=False,
            )
        )

    @staticmethod
    def register_session(
        db: Session,
        request: PortalSessionRegister,
    ):

        session = (
            SessionService.get_session(
                db=db,
                telegram_user_id=request.telegram_user_id,
                first_login=False,
            )
        )

        return (
            PortalSessionService
            ._build_session_response(
                session,
                request.telegram_user_id,
            )
        )