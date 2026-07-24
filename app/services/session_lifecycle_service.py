from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.pending_login import PendingLogin
from app.models.portal_session import PortalSession
from app.models.router_session import RouterSession

from app.services.pending_login_service import (
    PendingLoginService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.services.portal_session_service import (
    PortalSessionService,
)

from app.services.device_service import (
    DeviceService,
)


@dataclass(slots=True)
class SessionLifecycleResult:

    pending_login: PendingLogin

    router_session: RouterSession

    portal_session: PortalSession

    device: Device | None


class SessionLifecycleService:

    """
    Owns the BryanNet login lifecycle.

    PendingLogin
        ↓
    RouterSession
        ↓
    PortalSession
        ↓
    Device Online

    Everything succeeds together
    or everything rolls back.
    """

    @staticmethod
    def start_from_pending_login(
        db: Session,
        token: str,
    ) -> SessionLifecycleResult:

        try:

            #
            # ------------------------------------------------------
            # Pending Login
            # ------------------------------------------------------
            #

            pending_login = (

                PendingLoginService.get_by_token(

                    db,

                    token,

                )

            )

            PendingLoginService._validate_pending_login(
                pending_login,
            )

            device = pending_login.device

            #
            # ------------------------------------------------------
            # Router Session
            # ------------------------------------------------------
            #

            router_session = (

                RouterSessionService._create_from_pending_login(

                    db=db,

                    pending_login=pending_login,

                )

            )

            #
            # ------------------------------------------------------
            # Portal Session
            # ------------------------------------------------------
            #

            portal_session = (

                PortalSessionService._create_no_commit(

                    db=db,

                    customer=pending_login.customer,

                    router=pending_login.router,

                    router_account=pending_login.router_account,

                    router_session=router_session,

                    device=device,

                )

            )

            #
            # ------------------------------------------------------
            # Device
            # ------------------------------------------------------
            #

            if device:

                DeviceService._set_online_no_commit(
                    device,
                )

            #
            # ------------------------------------------------------
            # Consume token
            # ------------------------------------------------------
            #

            pending_login.status = (
                pending_login.status.CONSUMED
            )

            pending_login.consumed_at = (
                router_session.login_at
            )

            db.commit()

            db.refresh(
                pending_login,
            )

            db.refresh(
                router_session,
            )

            db.refresh(
                portal_session,
            )

            if device:

                db.refresh(
                    device,
                )

            return SessionLifecycleResult(

                pending_login=pending_login,

                router_session=router_session,

                portal_session=portal_session,

                device=device,

            )

        except Exception:

            db.rollback()

            raise
        
    @staticmethod
    def terminate_session(
        db: Session,
        *,
        router_session: RouterSession,
        reason: str | None = None,
    ) -> PortalSession | None:

        try:

            portal_session = (
                router_session.portal_session
            )

            RouterSessionService._set_inactive(
                router_session,
            )

            router_session.disconnect_reason = (
                reason
            )

            if portal_session:

                portal_session.is_active = False

                portal_session.logout_at = (
                    router_session.logout_at
                )

                portal_session.termination_reason = (
                    reason
                )

            device = router_session.device

            if device:

                active_sessions = (

                    db.query(
                        RouterSession,
                    )

                    .filter(

                        RouterSession.device_id
                        == device.device_id,

                        RouterSession.is_active.is_(True),

                        RouterSession.router_session_id
                        != router_session.router_session_id,

                    )

                    .count()

                )

                if active_sessions == 0:

                    DeviceService._set_offline(
                        device,
                    )

            db.commit()

            if portal_session:

                db.refresh(
                    portal_session,
                )

            db.refresh(
                router_session,
            )

            if device:

                db.refresh(
                    device,
                )

            return portal_session

        except Exception:

            db.rollback()

            raise