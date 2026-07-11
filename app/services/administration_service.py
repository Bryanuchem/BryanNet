from datetime import (
    date,
)

from sqlalchemy import (
    func,
)

from sqlalchemy.orm import (
    Session,
)

from app.models.admin_user import (
    AdminUser,
)

from app.models.admin_session import (
    AdminSession,
)

from app.models.audit_log import (
    AuditLog,
)

from app.models.role import (
    Role,
)

from app.schemas.administration import (
    AdministrationMetrics,
    AdministrationOverviewResponse,
    ActiveSessionItem,
    RecentAuditLogItem,
    SystemActivityItem,
)

from app.services.system_activity_service import (
    SystemActivityService,
)


class AdministrationService:

    # ==========================================================
    # Private Mappers
    # ==========================================================

    @staticmethod
    def _build_audit_log_item(
        audit_log,
    ):

        return RecentAuditLogItem(

            id=audit_log.audit_log_id,

            timestamp=audit_log.created_at,

            administrator=(

                audit_log.admin_user.username

                if audit_log.admin_user

                else "System"

            ),

            action=audit_log.action,

            module=audit_log.entity_type,

            target=(
                audit_log.target_name
                or "-"
            ),

            status=(
                audit_log.result.value.title()
            ),

        )

    @staticmethod
    def _build_active_session_item(
        session,
    ):

        return ActiveSessionItem(

            id=session.admin_session_id,

            administrator=(
                session.admin_user.username
            ),

            device=session.client_name,

            browser=(
                session.login_source.value.title()
            ),

            ip_address=(
                session.ip_address
                or "-"
            ),

            login_time=session.login_time,

            status=(

                "Active"

                if session.is_active

                else "Inactive"

            ),

        )

    @staticmethod
    def _build_system_activity_item(
        audit_log,
    ):

        return SystemActivityItem(

            id=audit_log.audit_log_id,

            timestamp=audit_log.created_at,

            administrator=(

                audit_log.admin_user.username

                if audit_log.admin_user

                else "System"

            ),

            action=audit_log.action,

            module=audit_log.entity_type,

            target=(

                audit_log.target_name

                or "-"

            ),

            status=(

                audit_log.result.value.title()

            ),

        )

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_metrics(
        db: Session,
    ):

        admin_users = (

            db.query(
                AdminUser,
            )

            .count()

        )

        login_sessions_today = (

            db.query(
                AdminSession,
            )

            .filter(

                func.date(
                    AdminSession.login_time,
                )
                == date.today(),

            )

            .count()

        )

        roles = (

            db.query(
                Role,
            )

            .count()

        )

        audit_events_today = (

            db.query(
                AuditLog,
            )

            .filter(

                func.date(
                    AuditLog.created_at,
                )

                ==

                date.today(),

            )

            .count()

        )
        
        system_events_today=(

            db.query(
                AuditLog,
            )

            .filter(

                AuditLog.admin_id.is_(None),

                func.date(
                    AuditLog.created_at,
                )

                ==

                date.today(),

            )

            .count()

        )        

        return AdministrationMetrics(

            admin_users=admin_users,

            login_sessions_today=login_sessions_today,

            roles=roles,

            audit_events_today=audit_events_today,

            system_events_today=system_events_today,

        )

    @staticmethod
    def _get_recent_audit_logs(
        db: Session,
    ):

        audit_logs = (

            db.query(
                AuditLog,
            )

            .order_by(
                AuditLog.created_at.desc(),
            )

            .limit(5)

            .all()

        )

        return [

            AdministrationService
            ._build_audit_log_item(
                audit_log,
            )

            for audit_log in audit_logs

        ]
        
    @staticmethod
    def _get_recent_login_sessions(
        db: Session,
    ):

        sessions = (

            db.query(
                AdminSession,
            )

            .order_by(
                AdminSession.login_time.desc(),
            )

            .limit(5)

            .all()

        )

        return [

            AdministrationService
            ._build_active_session_item(
                session,
            )

            for session in sessions

        ]

    @staticmethod
    def _get_system_activity(
        db: Session,
    ):

        audit_logs = (

            db.query(
                AuditLog,
            )

            .filter(
                AuditLog.admin_id.is_(None),
            )

            .order_by(
                AuditLog.created_at.desc(),
            )

            .limit(5)

            .all()

        )

        return [

            AdministrationService
            ._build_system_activity_item(
                audit_log,
            )

            for audit_log in audit_logs

        ]
    
    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_overview(
        db: Session,
    ) -> AdministrationOverviewResponse:

        return AdministrationOverviewResponse(

            metrics=(

                AdministrationService
                ._get_metrics(
                    db,
                )

            ),

            recent_audit_logs=(

                AdministrationService
                ._get_recent_audit_logs(
                    db,
                )

            ),

            active_sessions=(

                AdministrationService
                ._get_recent_login_sessions(
                    db,
                )

            ),

            system_activity=(

                AdministrationService
                ._get_system_activity(

                    db,

                )

            ),
        )