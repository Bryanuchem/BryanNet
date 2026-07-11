from fastapi import HTTPException


from app.models.audit_log import AuditLog


class SystemActivityService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_activity(
        db,
        audit_log_id,
    ):

        activity = (

            db.query(AuditLog)

            .filter(
                AuditLog.audit_log_id == audit_log_id,
                AuditLog.admin_id.is_(None)
            )

            .first()

        )

        if activity is None:

            raise HTTPException(

                status_code=404,

                detail="System activity not found.",

            )

        return activity

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_today_system_activity_count(
        db,
    ):

        from datetime import date

        return (

            db.query(AuditLog)

            .filter(

                AuditLog.admin_id.is_(None),
                AuditLog.created_at >= date.today(),

            )

            .count()

        )

    @staticmethod
    def get_system_activity(
        db,
        audit_log_id,
    ):

        return (

            SystemActivityService._find_activity(

                db,

                audit_log_id,

            )

        )

    @staticmethod
    def get_all_system_activity(

        db,

        page=1,

        page_size=25,

    ):

        query = (

            db.query(AuditLog)

            .filter(
                AuditLog.admin_id.is_(None),
            )

        )

        total = query.count()

        activities = (

            query

            .order_by(
                AuditLog.created_at.desc(),
            )

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

            "items": activities,

            "total": total,

            "page": page,

            "page_size": page_size,

            "pages": pages,

        }