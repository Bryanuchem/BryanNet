from typing import Literal

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

from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueOverviewItem,
    RecentActivityItem,
    SubscriptionBreakdownItem,
)

from app.services.dashboard_service import (
    DashboardService,
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ==========================================================
# Summary
# ==========================================================

@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_dashboard_summary(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.DASHBOARD_VIEW,
        ),
    ),
    
):

    return (
        DashboardService.get_summary(
            db,
        )
    )


# ==========================================================
# Revenue
# ==========================================================

@router.get(
    "/revenue-overview",
    response_model=list[RevenueOverviewItem],
)
def get_revenue_overview(
    period: Literal[
        "7d",
        "30d",
        "month",
        "12m",
    ] = "month",
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.DASHBOARD_VIEW,
        ),
    ),

):

    return (
        DashboardService.get_revenue_overview(
            db=db,
            period=period,
        )
    )


# ==========================================================
# Subscription Breakdown
# ==========================================================

@router.get(
    "/subscription-breakdown",
    response_model=list[SubscriptionBreakdownItem],
)
def get_subscription_breakdown(
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
        
    _=Depends(
        require_permission(
            Permissions.DASHBOARD_VIEW,
        ),
    ),

):

    return (
        DashboardService.get_subscription_breakdown(
            db,
        )
    )


# ==========================================================
# Recent Activity
# ==========================================================

@router.get(
    "/recent-activity",
    response_model=list[RecentActivityItem],
)
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(
        get_db,
    ),
    
    admin=Depends(
        get_current_admin,
    ),
    
    _=Depends(
        require_permission(
            Permissions.DASHBOARD_VIEW,
        ),
    ),
    
):

    return (
        DashboardService.get_recent_activity(
            db=db,
            limit=limit,
        )
    )