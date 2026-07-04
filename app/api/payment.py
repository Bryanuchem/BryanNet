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

from app.enums import (
    PaymentProvider,
    PaymentStatus,
    PaymentChannel,
)

from app.schemas.payment import (
    PaymentCreate,
    PaymentListItem,
    PaymentResponse,
    PaymentStatsResponse,
)

from app.services.payment_service import (
    PaymentService,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=201,
)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.create_payment(
            db=db,
            customer_id=payment.customer_id,
            plan_id=payment.plan_id,
            payment_provider=PaymentProvider(
                payment.payment_provider,
            ),
            payment_channel=payment.payment_channel,
            admin_id=admin.admin_user_id,
            payment_method=payment.payment_method,
        )
    )


@router.post(
    "/{payment_reference}/complete",
    response_model=PaymentResponse,
)
def complete_payment(
    payment_reference: str,
    gateway_transaction_id: str | None = None,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.complete_payment(
            db=db,
            payment_reference=payment_reference,
            admin_id=admin.admin_user_id,
            gateway_transaction_id=gateway_transaction_id,
        )
    )


@router.patch(
    "/{payment_reference}/cancel",
    response_model=PaymentResponse,
)
def cancel_payment(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.cancel_payment(
            db=db,
            payment_reference=payment_reference,
            admin_id=admin.admin_user_id,
        )
    )


@router.patch(
    "/{payment_reference}/refund",
    response_model=PaymentResponse,
)
def refund_payment(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.refund_payment(
            db=db,
            payment_reference=payment_reference,
            admin_id=admin.admin_user_id,
        )
    )


@router.patch(
    "/{payment_reference}/expire",
    response_model=PaymentResponse,
)
def expire_payment(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.expire_payment(
            db=db,
            payment_reference=payment_reference,
            admin_id=admin.admin_user_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        PaymentListItem
    ],
)
def get_payments(

    customer_id: int | None = None,

    payment_provider: PaymentProvider | None = None,

    payment_channel: PaymentChannel | None = None,

    payment_method: str | None = None,

    status: PaymentStatus | None = None,

    sort_by: str = "created_at",

    sort_order: str = "desc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),
):

    return (
        PaymentService.get_all_payments(

            db=db,

            page=page.page,

            page_size=page.page_size,

            customer_id=customer_id,

            payment_provider=payment_provider,

            payment_channel=payment_channel,

            payment_method=payment_method,

            status=status,

            sort_by=sort_by,

            sort_order=sort_order,

        )
    )


@router.get(
    "/summary",
    response_model=PaymentStatsResponse,
)
def get_payment_summary(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.get_payment_summary(
            db,
        )
    )


@router.get(
    "/{payment_reference}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.get_payment(
            db=db,
            payment_reference=payment_reference,
        )
    )


@router.get(
    "/customer/{customer_id}",
    response_model=list[PaymentResponse],
)
def get_customer_payments(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PaymentService.get_customer_payments(
            db=db,
            customer_id=customer_id,
        )
    )