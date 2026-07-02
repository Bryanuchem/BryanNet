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

from app.schemas.subscription import (
    SubscriptionAdminResponse,
    SubscriptionPurchase,
    SubscriptionResponse,
    SubscriptionStatusResponse,
)

from app.services.automation_service import (
    AutomationService,
)

from app.services.subscription_service import (
    SubscriptionService,
)


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/purchase",
    response_model=SubscriptionResponse,
)
def purchase_subscription(
    purchase: SubscriptionPurchase,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        SubscriptionService.create_subscription(
            db=db,
            customer_id=purchase.customer_id,
            plan_id=purchase.plan_id,
        )
    )


@router.patch(
    "/{subscription_id}/cancel",
    response_model=SubscriptionResponse,
)
def cancel_subscription(
    subscription_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.cancel_queued_subscription(
            db=db,
            subscription_id=subscription_id,
        )
    )


@router.post(
    "/process",
)
def process_subscription_jobs(
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


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[SubscriptionAdminResponse],
)
def get_all_subscriptions(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.get_all_subscriptions(
            db,
        )
    )


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionAdminResponse,
)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.get_subscription(
            db=db,
            subscription_id=subscription_id,
        )
    )


@router.get(
    "/customer/{customer_id}",
    response_model=list[SubscriptionAdminResponse],
)
def get_customer_subscriptions(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.get_customer_subscriptions(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/customer/{customer_id}/active",
    response_model=SubscriptionResponse,
)
def get_active_subscription(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.get_active_subscription(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/customer/{customer_id}/queued",
    response_model=list[SubscriptionResponse],
)
def get_queued_subscriptions(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        SubscriptionService.get_queued_subscriptions(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/customer/{customer_id}/status",
    response_model=SubscriptionStatusResponse,
)
def get_customer_subscription_status(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        SubscriptionService.get_customer_subscription_status(
            db=db,
            customer_id=customer_id,
        )
    )