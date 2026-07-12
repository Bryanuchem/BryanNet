from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.portal_subscription import (
    PortalSubscriptionActionRequest,
    PortalSubscriptionPurchase,
    PortalSubscriptionResponse,
)

from app.services.portal.subscription_service import (
    PortalSubscriptionService,
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["Portal Subscriptions"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/purchase",
    response_model=PortalSubscriptionResponse,
)
def purchase_subscription(
    request: PortalSubscriptionPurchase,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSubscriptionService.purchase_subscription(
            db,
            request,
        )
    )


@router.patch(
    "/{subscription_id}/cancel",
    response_model=PortalSubscriptionResponse,
)
def cancel_subscription(
    subscription_id: int,
    request: PortalSubscriptionActionRequest,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSubscriptionService.cancel_subscription(
            db,
            subscription_id,
            request,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/{telegram_user_id}",
    response_model=PortalSubscriptionResponse,
)
def get_subscription_status(
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalSubscriptionService.get_subscription_status(
            db,
            telegram_user_id,
        )
    )