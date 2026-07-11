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

from app.enums import (
    SubscriptionStatus,
)

from app.schemas.common import (
    JobResultResponse,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
)

from app.core.rate_limit import (
    limiter,
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
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_PURCHASE,
        ),
    ),
):

    return (
        SubscriptionService.create_subscription(
            db=db,
            customer_id=purchase.customer_id,
            plan_id=purchase.plan_id,
            admin_id=(
                admin.admin_user_id
                if admin
                else None
            ),
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
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_CANCEL,
        ),
    ),
):

    return (
        SubscriptionService.cancel_queued_subscription(
            db=db,
            subscription_id=subscription_id,
            admin_id=admin.admin_user_id,
        )
    )


@router.post(
    "/process",
    response_model=JobResultResponse,
)
@limiter.limit(
    "10/minute",
)
def process_subscription_jobs(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_PROCESS,
        ),
    ),
):

    result = (
        AutomationService.run_subscription_jobs(
            db,
        )
    )

    return JobResultResponse(
        processed=result["subscriptions_checked"],
        message="Subscription maintenance completed.",
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        SubscriptionAdminResponse
    ],
)
def get_subscriptions(

    search: str | None = None,

    customer_id: int | None = None,

    plan_id: int | None = None,

    status: SubscriptionStatus | None = None,

    sort_by: str = "created_at",

    sort_order: str = "desc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_VIEW,
        ),
    ),

):

    return (
        SubscriptionService.get_all_subscriptions(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

            customer_id=customer_id,

            plan_id=plan_id,

            status=status,

            sort_by=sort_by,

            sort_order=sort_order,

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
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_VIEW,
        ),
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
    response_model=list[
        SubscriptionAdminResponse
    ],
)
def get_customer_subscriptions(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_VIEW,
        ),
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
    response_model=list[
        SubscriptionResponse
    ],
)
def get_queued_subscriptions(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.SUBSCRIPTIONS_VIEW,
        ),
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