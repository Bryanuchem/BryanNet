from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.audit_log import (
    AuditLogResponse,
)

from app.services.audit_log_service import (
    AuditLogService,
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(

    search: str | None = None,

    action: str | None = None,

    result: str | None = None,

    admin_id: int | None = None,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.AUDIT_LOGS_VIEW,
        ),
    ),

):

    return (
        AuditLogService.get_all_logs(

            db=db,

            search=search,

            action=action,

            result=result,

            admin_id=admin_id,

        )
    )

@router.get(
    "/{audit_log_id}",
    response_model=AuditLogResponse,
)
def get_audit_log(

    audit_log_id: int,

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.AUDIT_LOGS_VIEW,
        ),
    ),

):
    return (
        AuditLogService.get_audit_log(
            db,
            audit_log_id,
        )
    )