from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.orm import (
    Session,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.services.automation_service import (
    AutomationService,
)

from app.schemas.common import (
    JobResultResponse,
)

from app.core.rate_limit import (
    limiter,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    AUTOMATION_RUN_ALL,
    AUTOMATION_PAYMENTS,
    AUTOMATION_SUBSCRIPTIONS,
    AUTOMATION_DEVICES,
    AUTOMATION_REMINDERS,
)

from app.enums.audit_result import (
    AuditResult,
)

router = APIRouter(
    prefix="/automation",
    tags=["Automation"],
)


# ==========================================================
# Automation
# ==========================================================

@router.post(
    "/all",
)
@limiter.limit(
    "10/minute",
)
def run_all_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.AUTOMATION_RUN,
        ),
    ),
):

    result = (
        AutomationService.run_all_jobs(
            db,
        )
    )

    AuditLogService.log_system_action(

        db=db,

        admin=admin,

        action=AUTOMATION_RUN_ALL,

        entity_type="Automation",

        target_name="All Jobs",

        result=AuditResult.SUCCESS,

        description=(
            "Executed all automation jobs."
        ),

        new_values=result,

    )

    db.commit()

    return result


@router.post(
    "/payments",
    response_model=JobResultResponse,
)
@limiter.limit(
    "10/minute",
)
def run_payment_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.AUTOMATION_RUN,
        ),
    ),
):

    result = (
        AutomationService.run_payment_jobs(
            db,
        )
    )

    AuditLogService.log_system_action(

        db=db,

        admin=admin,

        action=AUTOMATION_PAYMENTS,

        entity_type="Automation",

        target_name="Payment Automation",

        result=AuditResult.SUCCESS,

        description=(
            "Executed payment automation."
        ),

        new_values=result,

    )

    db.commit()

    return JobResultResponse(
        processed=result["processed"],
        message="Payment maintenance completed.",
    )


@router.post(
    "/subscriptions",
    response_model=JobResultResponse,
)
@limiter.limit(
    "10/minute",
)
def run_subscription_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.AUTOMATION_RUN,
        ),
    ),
):

    result = (
        AutomationService.run_subscription_jobs(
            db,
        )
    )

    AuditLogService.log_system_action(

        db=db,

        admin=admin,

        action=AUTOMATION_SUBSCRIPTIONS,

        entity_type="Automation",

        target_name="Subscription Automation",

        result=AuditResult.SUCCESS,

        description=(
            "Executed subscription automation."
        ),

        new_values=result,

    )

    db.commit()

    return JobResultResponse(
        processed=result["processed"],
        message="Subscription maintenance completed.",
    )


@router.post(
    "/routers",
    response_model=JobResultResponse,
)
@limiter.limit(
    "10/minute",
)
def run_router_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.AUTOMATION_RUN,
        ),
    ),
):

    result = (
        AutomationService.run_router_jobs(
            db,
        )
    )

    AuditLogService.log_system_action(

        db=db,

        admin=admin,

        action=AUTOMATION_DEVICES,

        entity_type="Automation",

        target_name="Router Automation",

        result=AuditResult.SUCCESS,

        description=(
            "Executed router automation."
        ),

        new_values=result,

    )

    db.commit()

    return JobResultResponse(
        processed=result["processed"],
        message="Router maintenance completed.",
    )


@router.post(
    "/notifications",
    response_model=JobResultResponse,
)
@limiter.limit(
    "10/minute",
)
def run_notification_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.AUTOMATION_RUN,
        ),
    ),
):

    result = (
        AutomationService.run_notification_jobs(
            db,
        )
    )

    AuditLogService.log_system_action(

        db=db,

        admin=admin,

        action=AUTOMATION_REMINDERS,

        entity_type="Automation",

        target_name="Notification Automation",

        result=AuditResult.SUCCESS,

        description=(
            "Executed notification scheduling."
        ),

        new_values=result,

    )

    db.commit()

    return JobResultResponse(
        processed=result["processed"],
        message="Notification scheduling completed.",
    )