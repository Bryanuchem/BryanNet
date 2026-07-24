from datetime import (
    UTC,
    datetime,
)

from fastapi import (
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.models.customer import (
    Customer,
)

from app.models.device import (
    Device,
)

from app.models.portal_session import (
    PortalSession,
)

from app.models.router import (
    Router,
)

from app.models.router_account import (
    RouterAccount,
)

from app.models.router_session import (
    RouterSession,
)


class PortalSessionService:

    """
    Manages BryanNet portal sessions.

    Responsibilities

    - Create portal session
    - Retrieve portal session
    - Extend portal session
    - Terminate portal session

    This service deliberately
    does NOT:

    - Authenticate customers
    - Register devices
    - Login to RouterOS
    - Render HTML
    """

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_session(
        db: Session,
        portal_session_id: int,
    ):

        session = (

            db.query(
                PortalSession,
            )

            .filter(

                PortalSession.portal_session_id
                == portal_session_id,

            )

            .first()

        )

        if not session:

            raise HTTPException(

                status_code=404,

                detail="Portal session not found.",

            )

        return session

    @staticmethod
    def _find_active_session(
        db: Session,
        *,
        router_session_id: int,
    ):

        return (

            db.query(
                PortalSession,
            )

            .filter(

                PortalSession.router_session_id
                == router_session_id,

                PortalSession.is_active.is_(True),

            )

            .first()

        )

    @staticmethod
    def _create_no_commit(
        db,
        *,
        customer,
        router,
        router_account,
        router_session,
        device=None,
    ):

        existing = (

            PortalSessionService._find_active_session(

                db,

                router_session_id=(
                    router_session.router_session_id
                ),

            )

        )

        if existing:

            return existing

        session = PortalSession(

            customer_id=customer.customer_id,

            router_id=router.router_id,

            router_account_id=(
                router_account.router_account_id
            ),

            router_session_id=(
                router_session.router_session_id
            ),

            device_id=(
                device.device_id
                if device
                else None
            ),

            login_at=router_session.login_at,

            is_active=True,

        )

        db.add(
            session,
        )

        db.flush()

        return session

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        db: Session,
        *,
        customer: Customer,
        router: Router,
        router_account: RouterAccount,
        router_session: RouterSession,
        device: Device | None = None,
    ):

        existing = (

            PortalSessionService

            ._find_active_session(

                db,

                router_session_id=(
                    router_session.router_session_id
                ),

            )

        )

        # ======================================================
        # Idempotency
        # ======================================================

        if existing:

            return existing

        session = PortalSession(

            customer_id=customer.customer_id,

            router_id=router.router_id,

            router_account_id=(
                router_account.router_account_id
            ),

            router_session_id=(
                router_session.router_session_id
            ),

            device_id=(

                device.device_id

                if device

                else None

            ),

            login_at=(

                router_session.login_at

                or datetime.now(
                    UTC,
                )

            ),

            is_active=True,

        )

        db.add(
            session,
        )

        db.commit()

        db.refresh(
            session,
        )

        return session

    @staticmethod
    def extend(
        db: Session,
        *,
        portal_session: PortalSession,
    ):

        #
        # Reserved for future heartbeat /
        # activity updates.
        #

        db.commit()

        db.refresh(
            portal_session,
        )

        return portal_session

    @staticmethod
    def terminate(
        db: Session,
        *,
        router_session_id: int,
        termination_reason: str | None = None,
    ):

        portal_session = (

            PortalSessionService

            ._find_active_session(

                db,

                router_session_id=router_session_id,

            )

        )

        # ======================================================
        # Idempotency
        # ======================================================

        if not portal_session:

            return None

        portal_session.logout_at = (

            datetime.now(
                UTC,
            )

        )

        portal_session.is_active = False

        portal_session.termination_reason = (
            termination_reason
        )

        db.commit()

        db.refresh(
            portal_session,
        )

        return portal_session

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get(
        db: Session,
        *,
        session_id: int,
    ):

        return (

            PortalSessionService

            ._find_session(

                db,

                session_id,

            )

        )

    @staticmethod
    def get_active(
        db: Session,
        *,
        router_session_id: int,
    ):

        return (

            PortalSessionService

            ._find_active_session(

                db,

                router_session_id=router_session_id,

            )

        )