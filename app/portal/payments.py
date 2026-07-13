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

from app.database.dependencies import (
    get_db,
)

from app.schemas.portal_payment import (
    PortalPaymentCreate,
    PortalPaymentResponse,
    PortalPaymentDetailResponse,
)

from app.services.portal.payment_service import (
    PortalPaymentService,
)


router = APIRouter(
    prefix="/payments",
    tags=["Portal Payments"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/initialize",
    response_model=PortalPaymentResponse,
)
def initialize_payment(
    request: PortalPaymentCreate,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalPaymentService.initialize_payment(
            db,
            request,
        )
    )

@router.post(
    "/verify/{payment_reference}",
    response_model=PortalPaymentResponse,
)
def verify_payment(
    payment_reference: str,
    telegram_user_id: int,
    db: Session = Depends(get_db),
):

    return (
        PortalPaymentService.verify_payment(
            db,
            telegram_user_id,
            payment_reference,
        )
    )

@router.post(
    "/retry/{payment_reference}",
    response_model=PortalPaymentResponse,
)
def retry_payment(
    payment_reference: str,
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalPaymentService.retry_payment(
            db,
            telegram_user_id,
            payment_reference,
        )
    )

# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/{payment_reference}",
    response_model=PortalPaymentResponse,
)
def get_payment(
    payment_reference: str,
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalPaymentService.get_payment(
            db,
            telegram_user_id,
            payment_reference,
        )
    )


@router.get(
    "/customer/{telegram_user_id}",
    response_model=list[
        PortalPaymentResponse
    ],
)
def get_customer_payments(
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalPaymentService.get_customer_payments(
            db,
            telegram_user_id,
        )
    )
    
@router.get(
    "/{payment_reference}/receipt",
)
def get_receipt(
    payment_reference: str,
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    pdf = (

        PortalPaymentService.get_receipt(

            db,

            telegram_user_id,

            payment_reference,

        )

    )

    return StreamingResponse(

        pdf,

        media_type="application/pdf",

        headers={

            "Content-Disposition": (

                "attachment; "

                f'filename="{payment_reference}.pdf"'

            ),

        },

    )
    
@router.get(
    "/success/{payment_reference}",
    response_model=PortalPaymentResponse,
)
def get_success_payment(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalPaymentService
        .get_payment_by_reference(
            db,
            payment_reference,
        )
    )
    
@router.get(
    "/details/{payment_reference}",
    response_model=PortalPaymentDetailResponse,
)
def get_payment_details(
    payment_reference: str,
    db: Session = Depends(
        get_db,
    ),
):

    return (

        PortalPaymentService

        .get_payment_details(

            db,

            payment_reference,

        )

    )