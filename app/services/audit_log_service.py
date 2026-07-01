from fastapi import HTTPException

from app.models.audit_log import AuditLog


class AuditLogService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_log(
        db,
        audit_log_id,
    ):

        audit_log = (
            db.query(AuditLog)
            .filter(
                AuditLog.id == audit_log_id
            )
            .first()
        )

        if not audit_log:

            raise HTTPException(
                status_code=404,
                detail="Audit log not found.",
            )

        return audit_log

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def log_action(
        db,
        admin_id,
        admin_session_id,
        action,
        entity_type,
        entity_id,
        description,
        old_values=None,
        new_values=None,
        ip_address=None,
        user_agent=None,
    ):

        audit_log = AuditLog(

            admin_id=admin_id,

            admin_session_id=admin_session_id,

            action=action,

            entity_type=entity_type,

            entity_id=entity_id,

            description=description,

            old_values=old_values,

            new_values=new_values,

            ip_address=ip_address,

            user_agent=user_agent,

        )

        db.add(audit_log)

        db.commit()

        db.refresh(audit_log)

        return audit_log

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_log(
        db,
        audit_log_id,
    ):

        return (
            AuditLogService._find_log(
                db,
                audit_log_id,
            )
        )

    @staticmethod
    def get_logs(
        db,
    ):

        return (
            db.query(AuditLog)
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_logs_by_admin(
        db,
        admin_id,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.admin_id == admin_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_logs_by_entity(
        db,
        entity_type,
        entity_id,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id,
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_logs_by_action(
        db,
        action,
    ):

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.action == action
            )
            .order_by(
                AuditLog.created_at.desc()
            )
            .all()
        )
        
    @staticmethod
    def get_recent_activity(
        db,
        limit=10,
    ):

        return (
            db.query(AuditLog)
            .order_by(
                AuditLog.created_at.desc()
            )
            .limit(limit)
            .all()
        )        