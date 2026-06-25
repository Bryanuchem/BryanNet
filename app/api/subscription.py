from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.subscription import (
    SubscriptionPurchase,
    SubscriptionResponse,
    SubscriptionStatusResponse

)

from app.services.subscription_service import (
    SubscriptionService
)

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


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