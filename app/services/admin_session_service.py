from datetime import datetime, UTC

from fastapi import HTTPException

from app.models.admin_session import AdminSession

from app.enums import (
    LoginSource,
    LogoutReason,
)

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
                AdminSession.admin_session_id == admin_session_id,
            )
            .first()
        )

        if session is None:

            raise HTTPException(
                status_code=404,
                detail="Admin session not found.",
            )

        return session

    @staticmethod
    def _get_session(
        db,
        admin_session_id,
        admin_user_id,
    ):

        return (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_session_id == admin_session_id,
                AdminSession.admin_user_id == admin_user_id,
            )
            .first()
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
    def create_session(
        db,
        admin_user_id,
        ip_address=None,
        user_agent=None,
        *,
        login_source=LoginSource.WEB,
        client_name="Dashboard",
    ):

        now = datetime.now(
            UTC,
        )

        (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_user_id == admin_user_id,
                AdminSession.is_active.is_(True),
            )
            .update(
                {
                    AdminSession.is_active: False,
                    AdminSession.logout_time: now,
                    AdminSession.last_activity: now,
                    AdminSession.logout_reason: LogoutReason.NEW_LOGIN,
                },
                synchronize_session=False,
            )
        )

        session = AdminSession(

            admin_user_id=admin_user_id,

            login_time=now,

            last_activity=now,

            ip_address=ip_address,

            user_agent=user_agent,

            login_source=login_source,

            client_name=client_name,

            is_active=True,

        )

        db.add(
            session,
        )

        db.flush()

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

        session.last_activity = datetime.now(
            UTC,
        )

        return (
            AdminSessionService._finalize_session_change(
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

        now = datetime.now(
            UTC,
        )

        session.is_active = False

        session.logout_time = now

        session.last_activity = now

        session.logout_reason = LogoutReason.MANUAL

        return (
            AdminSessionService._finalize_session_change(
                db,
                session,
            )
        )

    @staticmethod
    def close_all_sessions(
        db,
        admin_user_id,
    ):

        now = datetime.now(
            UTC,
        )

        sessions = (
            db.query(AdminSession)
            .filter(
                AdminSession.admin_user_id == admin_user_id,
                AdminSession.is_active.is_(True),
            )
            .all()
        )

        for session in sessions:

            session.is_active = False

            session.logout_time = now

            session.last_activity = now

            session.logout_reason = LogoutReason.CLOSE_ALL

        db.commit()

        return sessions

    @staticmethod
    def _finalize_session_change(
        db,
        session,
    ):

        db.commit()

        db.refresh(
            session,
        )

        return session

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
    def validate_active_session(
        db,
        admin_session_id,
        admin_user_id,
    ):

        session = (
            AdminSessionService._get_session(
                db=db,
                admin_session_id=admin_session_id,
                admin_user_id=admin_user_id,
            )
        )

        if session is None:

            raise HTTPException(
                status_code=401,
                detail="Session not found.",
            )

        if not session.is_active:

            raise HTTPException(
                status_code=401,
                detail="Session has expired.",
            )

        return session

    @staticmethod
    def touch_active_session(
        session,
    ):

        session.last_activity = datetime.now(
            UTC,
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
        page=1,
        page_size=25,
        admin_user_id=None,
        is_active=None,
        sort_by="login_time",
        sort_order="desc",
    ):

        query = (
            db.query(AdminSession)
        )

        if admin_user_id is not None:

            query = query.filter(
                AdminSession.admin_user_id == admin_user_id,
            )

        if is_active is not None:

            query = query.filter(
                AdminSession.is_active == is_active,
            )

        sort_column = {

            "login_time":
                AdminSession.login_time,

            "last_activity":
                AdminSession.last_activity,

        }.get(

            sort_by,

            AdminSession.login_time,

        )

        query = (
            AdminSessionService._apply_sort(
                query,
                sort_column,
                sort_order,
            )
        )

        return (

            query

            .offset(
                (page - 1) * page_size,
            )

            .limit(
                page_size,
            )

            .all()

        )