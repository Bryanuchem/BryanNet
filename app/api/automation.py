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

from app.services.automation_service import (
    AutomationService,
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
def run_all_jobs(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AutomationService.run_all_jobs(
            db,
        )
    )


@router.post(
    "/payments",
)
def run_payment_jobs(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AutomationService.run_payment_jobs(
            db,
        )
    )


@router.post(
    "/subscriptions",
)
def run_subscription_jobs(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AutomationService.run_subscription_jobs(
            db,
        )
    )


@router.post(
    "/routers",
)
def run_router_jobs(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AutomationService.run_router_jobs(
            db,
        )
    )


@router.post(
    "/notifications",
)
def run_notification_jobs(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        AutomationService.run_notification_jobs(
            db,
        )
    )