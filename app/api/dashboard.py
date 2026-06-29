from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueOverviewItem,
    SubscriptionBreakdownItem,
    RecentActivityItem,
)

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def get_dashboard_summary(
    db: Session = Depends(get_db)
):

    return DashboardService.get_summary(
        db=db
    )


@router.get(
    "/revenue-overview",
    response_model=list[RevenueOverviewItem]
)
def get_revenue_overview(
    period: str = "month",
    db: Session = Depends(get_db)
):

    return DashboardService.get_revenue_overview(
        db=db,
        period=period
    )


@router.get(
    "/subscription-breakdown",
    response_model=list[SubscriptionBreakdownItem]
)
def get_subscription_breakdown(
    db: Session = Depends(get_db)
):

    return DashboardService.get_subscription_breakdown(
        db=db
    )

  
@router.get(
    "/recent-activity",
    response_model=list[RecentActivityItem],
)
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
):

    return DashboardService.get_recent_activity(
        db=db,
        limit=limit,
    )    
