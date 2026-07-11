from datetime import datetime, UTC

from fastapi import HTTPException

from app.models.admin_session import AdminSession

from app.enums import (
    LoginSource,
    LogoutReason,
)

from sqlalchemy.orm import (
    joinedload,
)

from app.models.admin_user import (
    AdminUser,
)

from app.schemas.admin_session import (
    AdminSessionResponse,
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
            .options(
                joinedload(
                    AdminSession.admin_user,
                ),
            )
            .filter(
                AdminSession.admin_session_id == admin_session_id,
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

    @staticmethod
    def _build_session_response(
        session,
    ):

        return AdminSessionResponse(

            admin_session_id=session.admin_session_id,

            admin_user_id=session.admin_user_id,

            administrator=(

                session.admin_user.username

                if session.admin_user

                else "-"

            ),

            login_time=session.login_time,

            last_activity=session.last_activity,

            logout_time=session.logout_time,

            ip_address=session.ip_address,

            user_agent=session.user_agent,

            login_source=session.login_source,

            client_name=session.client_name,

            logout_reason=session.logout_reason,

            is_active=session.is_active,

            created_at=session.created_at,

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

        session = (

            AdminSessionService._find_session(

                db,

                admin_session_id,

            )

        )

        return (

            AdminSessionService
            ._build_session_response(

                session,

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

        search=None,

        admin_user_id=None,

        is_active=None,

        device=None,

        browser=None,

        sort_by="login_time",

        sort_order="desc",

    ):

        query = (

            db.query(
                AdminSession,
            )

            .join(

                AdminUser,

                AdminSession.admin_user_id
                == AdminUser.admin_user_id,

            )

            .options(

                joinedload(
                    AdminSession.admin_user,
                ),

            )

        )

        if search:

            query = query.filter(

                (

                    AdminUser.username.ilike(
                        f"%{search}%",
                    )

                )

                |

                (

                    AdminSession.ip_address.ilike(
                        f"%{search}%",
                    )

                )

                |

                (

                    AdminSession.client_name.ilike(
                        f"%{search}%",
                    )

                )

            )

        if admin_user_id is not None:

            query = query.filter(

                AdminSession.admin_user_id
                == admin_user_id,

            )

        if is_active is not None:

            query = query.filter(

                AdminSession.is_active
                == is_active,

            )

        if device:

            query = query.filter(

                AdminSession.client_name
                == device,

            )

        if browser:

            query = query.filter(

                AdminSession.login_source
                == browser,

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

        total = query.count()

        sessions = (

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

            "items": [

                AdminSessionService
                ._build_session_response(

                    session,

                )

                for session in sessions

            ],

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": pages,

        }