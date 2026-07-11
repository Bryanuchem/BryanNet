from typing import Any

from fastapi import HTTPException

from sqlalchemy.orm import (

    Session,

    joinedload,

)

from app.models.audit_log import AuditLog

from app.schemas.audit_log import (
    AuditLogResponse,
)

from app.enums.audit_result import AuditResult



class AuditLogService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_log(
        db: Session,
        audit_log_id: int,
    ) -> AuditLog:

        audit_log = (

            db.query(
                AuditLog,
            )

            .options(

                joinedload(
                    AuditLog.admin_user,
                ),

            )

            .filter(

                AuditLog.audit_log_id == audit_log_id,

            )

            .first()

        )

        if audit_log is None:

            raise HTTPException(

                status_code=404,

                detail="Audit log not found.",

            )

        return audit_log

    @staticmethod
    def _build_audit_log_response(
        audit_log: AuditLog,
    ) -> AuditLogResponse:

        return AuditLogResponse(

            audit_log_id=audit_log.audit_log_id,

            admin_id=audit_log.admin_id,

            administrator=(

                audit_log.admin_user.username

                if audit_log.admin_user

                else "System"

            ),

            admin_session_id=audit_log.admin_session_id,

            action=audit_log.action,

            entity_type=audit_log.entity_type,

            entity_id=audit_log.entity_id,

            target_name=audit_log.target_name,

            result=audit_log.result,

            description=audit_log.description,

            old_values=audit_log.old_values,

            new_values=audit_log.new_values,

            ip_address=audit_log.ip_address,

            user_agent=audit_log.user_agent,

            created_at=audit_log.created_at,

        )

    @staticmethod
    def log_admin_action(
        db: Session,
        admin_id: int,
        action: str,
        description: str,
        *,
        admin_session_id: int | None = None,
        target_name: str | None = None,
        entity_type: str = "AdminUser",
        entity_id: int | None = None,
        result: AuditResult = AuditResult.SUCCESS,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:

        return AuditLogService.log_action(
            
            db=db,

            admin_id=admin_id,

            admin_session_id=admin_session_id,

            action=action,

            entity_type=entity_type,

            entity_id=entity_id,

            target_name=target_name,

            result=result,

            description=description,

            old_values=old_values,

            new_values=new_values,

            ip_address=ip_address,

            user_agent=user_agent,

        )

    @staticmethod
    def log_system_action(
        db: Session,
        action: str,
        description: str,
        *,
        admin=None,
        session=None,
        entity_type: str = "System",
        entity_id: int | None = None,
        target_name: str | None = None,
        result: AuditResult = AuditResult.INFO,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
    ) -> AuditLog:

        return AuditLogService.log_action(

            db=db,

            admin_id=(
                admin.admin_user_id
                if admin
                else None
            ),

            admin_session_id=(
                session.admin_session_id
                if session
                else None
            ),

            action=action,

            entity_type=entity_type,

            entity_id=entity_id,

            target_name=target_name,

            result=result,

            description=description,

            old_values=old_values,

            new_values=new_values,

        )



    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def log_action(
        db: Session,
        admin_id: int | None,
        action: str,
        entity_type: str,
        description: str,
        entity_id: int | None = None,
        target_name: str | None = None,
        result: AuditResult = AuditResult.SUCCESS,
        admin_session_id: int | None = None,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(

            admin_id=admin_id,

            admin_session_id=admin_session_id,

            action=action,

            entity_type=entity_type,

            entity_id=entity_id,
            
            target_name=target_name,

            result=result,

            description=description,

            old_values=old_values,

            new_values=new_values,

            ip_address=ip_address,

            user_agent=user_agent,

        )

        db.add(audit_log)

        db.flush()

        return audit_log

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_audit_log(
        db: Session,
        audit_log_id: int,
    ) -> AuditLogResponse:

        audit_log = (

            AuditLogService._find_log(

                db=db,

                audit_log_id=audit_log_id,

            )

        )

        return (

            AuditLogService._build_audit_log_response(

                audit_log,

            )

        )

    @staticmethod
    def get_all_logs(

        db: Session,

        search: str | None = None,

        action: str | None = None,

        result: str | None = None,

        admin_id: int | None = None,

    ) -> list[AuditLogResponse]:

        query = (

            db.query(
                AuditLog,
            )

            .options(

                joinedload(
                    AuditLog.admin_user,
                ),

            )

        )

        if search:

            query = query.filter(

                AuditLog.description.ilike(
                    f"%{search}%",
                )

            )

        if action:

            query = query.filter(

                AuditLog.action == action,

            )

        if result:

            query = query.filter(

                AuditLog.result == result,

            )

        if admin_id is not None:

            query = query.filter(

                AuditLog.admin_id == admin_id,

            )

        audit_logs = (

            query

            .order_by(

                AuditLog.created_at.desc(),

            )

            .all()

        )

        return [

            AuditLogService

            ._build_audit_log_response(

                audit_log,

            )

            for audit_log in audit_logs

        ]

    @staticmethod
    def get_logs_by_admin(
        db: Session,
        admin_id: int,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.admin_id == admin_id,
            )
            .order_by(
                AuditLog.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def get_logs_by_entity(
        db: Session,
        entity_type: str,
        entity_id: int,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.entity_type == entity_type,
                AuditLog.entity_id == entity_id,
            )
            .order_by(
                AuditLog.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def get_logs_by_action(
        db: Session,
        action: str,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .filter(
                AuditLog.action == action,
            )
            .order_by(
                AuditLog.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def get_recent_activity(
        db: Session,
        limit: int = 10,
    ) -> list[AuditLog]:

        return (
            db.query(AuditLog)
            .order_by(
                AuditLog.created_at.desc(),
            )
            .limit(limit)
            .all()
        )