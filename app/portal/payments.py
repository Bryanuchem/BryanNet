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

from app.schemas.portal_payment import (
    PortalPaymentCreate,
    PortalPaymentResponse,
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