from datetime import datetime, UTC

from fastapi import HTTPException

from app.models.admin_session import AdminSession


class AdminSessionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_session(
        db,
        admin_session_id,
    ):

        session = (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_session_id
                == admin_session_id
            )
            .first()
        )

        if not session:

            raise HTTPException(
                status_code=404,
                detail="Admin session not found.",
            )

        return session

    @staticmethod
    def _get_active_session(
        db,
        admin_user_id,
    ):

        return (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_user_id == admin_user_id,
                AdminSession.is_active.is_(True),
            )
            .order_by(
                AdminSession.login_time.desc()
            )
            .first()
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_session(
        db,
        admin_user_id,
        ip_address=None,
        user_agent=None,
    ):

        session = AdminSession(

            admin_user_id=admin_user_id,

            login_time=datetime.now(UTC),

            last_activity=datetime.now(UTC),

            ip_address=ip_address,

            user_agent=user_agent,

            is_active=True,

        )

        db.add(session)

        db.commit()

        db.refresh(session)

        return session

    @staticmethod
    def update_activity(
        db,
        admin_session_id,
    ):

        session = (
            AdminSessionService._find_session(
                db,
                admin_session_id,
            )
        )

        session.last_activity = (
            datetime.now(UTC)
        )

        return (
            AdminSessionService
            ._finalize_session_change(
                db,
                session,
            )
        )

    @staticmethod
    def close_session(
        db,
        admin_session_id,
    ):

        session = (
            AdminSessionService._find_session(
                db,
                admin_session_id,
            )
        )

        session.logout_time = (
            datetime.now(UTC)
        )

        session.is_active = False

        return (
            AdminSessionService
            ._finalize_session_change(
                db,
                session,
            )
        )

    @staticmethod
    def close_all_sessions(
        db,
        admin_user_id,
    ):

        sessions = (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_user_id == admin_user_id,
                AdminSession.is_active.is_(True),
            )
            .all()
        )

        now = datetime.now(UTC)

        for session in sessions:

            session.logout_time = now

            session.last_activity = now

            session.is_active = False

        return (
            AdminSessionService
            ._finalize_session_change(
                db,
                session,
            )
)

    @staticmethod
    def _finalize_session_change(
        db,
        session,
    ):

        return (
            AdminSessionService
            ._finalize_session_change(
                db,
                session,
            )
        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_session(
        db,
        admin_session_id,
    ):

        return (
            AdminSessionService._find_session(
                db,
                admin_session_id,
            )
        )

    @staticmethod
    def get_active_session(
        db,
        admin_user_id,
    ):

        return (
            AdminSessionService._get_active_session(
                db,
                admin_user_id,
            )
        )

    @staticmethod
    def get_admin_sessions(
        db,
        admin_user_id,
    ):

        return (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_user_id == admin_user_id,
            )
            .order_by(
                AdminSession.login_time.desc(),
            )
            .all()
        )

    @staticmethod
    def get_active_sessions(
        db,
    ):

        return (
            db.query(AdminSession)
            .filter(
                AdminSession.is_active.is_(True),
            )
            .order_by(
                AdminSession.last_activity.desc(),
            )
            .all()
        )

    @staticmethod
    def get_all_sessions(
        db,
    ):

        return (
            db.query(AdminSession)
            .order_by(
                AdminSession.login_time.desc(),
            )
            .all()
        )