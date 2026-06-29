from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.subscription import (
    SubscriptionPurchase,
    SubscriptionResponse,
    SubscriptionStatusResponse,
    SubscriptionAdminResponse,
    SubscriptionUpdate,
    SubscriptionStatusUpdate
)

from app.services.subscription_service import (
    SubscriptionService
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


# ==========================================================
# Admin Dashboard Endpoints
# ==========================================================

@router.get(
    "/",
    response_model=list[SubscriptionAdminResponse]
)
def get_subscriptions(
    db: Session = Depends(get_db)
):

    return SubscriptionService.get_all_subscriptions(
        db=db
    )


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionAdminResponse
)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    return SubscriptionService.get_subscription(
        db=db,
        subscription_id=subscription_id
    )


@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionResponse
)
def update_subscription(
    subscription_id: int,
    subscription: SubscriptionUpdate,
    db: Session = Depends(get_db)
):

    return SubscriptionService.update_subscription(
        db=db,
        subscription_id=subscription_id,
        subscription_data=subscription
    )


@router.patch(
    "/{subscription_id}/status",
    response_model=SubscriptionResponse
)
def update_subscription_status(
    subscription_id: int,
    status: SubscriptionStatusUpdate,
    db: Session = Depends(get_db)
):

    return SubscriptionService.update_subscription_status(
        db=db,
        subscription_id=subscription_id,
        status=status.status
    )


@router.post(
    "/{subscription_id}/renew",
    response_model=SubscriptionResponse
)
def renew_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    return SubscriptionService.renew_subscription(
        db=db,
        subscription_id=subscription_id
    )

@router.delete(
    "/{subscription_id}"
)
def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):

    return SubscriptionService.delete_subscription(
        db=db,
        subscription_id=subscription_id
    )


# ==========================================================
# Telegram Bot Endpoints
# ==========================================================

@router.post(
    "/purchase",
    response_model=SubscriptionResponse
)
def purchase_subscription(
    purchase: SubscriptionPurchase,
    db: Session = Depends(get_db)
):

    return SubscriptionService.buy_plan(
        db=db,
        customer_id=purchase.customer_id,
        plan_id=purchase.plan_id
    )


@router.get(
    "/status/{customer_id}",
    response_model=SubscriptionStatusResponse
)
def get_subscription_status(
    customer_id: int,
    db: Session = Depends(get_db)
):

    return SubscriptionService.get_status(
        db=db,
        customer_id=customer_id
    )


@router.post(
    "/process"
)
def process_subscriptions(
    db: Session = Depends(get_db)
):

    return SubscriptionService.process_subscriptions(
        db=db
    )