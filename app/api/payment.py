from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.responses import (
    StreamingResponse,
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

from app.enums import (
    PaymentProvider,
    PaymentStatus,
    PaymentChannel,
)

from app.schemas.payment import (
    PaymentCreate,
    PaymentListItem,
    PaymentResponse,
    PaymentStatsResponse
)

from app.services.payment_service import (
    PaymentService,
)

from app.services.payment_document_service import (
    PaymentDocumentService,
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_CREATE,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_COMPLETE,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_CANCEL,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_REFUND,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_EXPIRE,
        ),
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

    search: str | None = None,

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

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.PAYMENTS_VIEW,
        ),
    ),

):

    return (
        PaymentService.get_all_payments(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

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
    "/{payment_reference}/receipt",
)
def get_payment_receipt(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_VIEW,
        ),
    ),
):

    pdf = (
        PaymentDocumentService.generate_receipt_pdf(
            db=db,
            payment_reference=payment_reference,
        )
    )

    return StreamingResponse(

        pdf,

        media_type="application/pdf",

        headers={

            "Content-Disposition": (

                f'inline; '

                f'filename="{payment_reference}.pdf"'

            ),

        },

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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PAYMENTS_VIEW,
        ),
    ),
):

    return (
        PaymentService.get_customer_payments(
            db=db,
            customer_id=customer_id,
        )
    )