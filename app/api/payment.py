from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
    PaymentListItem,
    PaymentStatsResponse,
)

from app.services.payment_service import (
    PaymentService,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.get(
    "/",
    response_model=list[PaymentListItem],
)
def get_payments(
    search: str | None = None,
    payment_channel: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):

    return PaymentService.get_all_payments(
        db=db,
        search=search,
        payment_channel=payment_channel,
        status=status,
    )


@router.get(
    "/summary",
    response_model=PaymentStatsResponse,
)
def get_payment_summary(
    db: Session = Depends(get_db),
):

    return PaymentService.get_payment_summary(
        db=db,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):

    payment = PaymentService.get_payment(
        db=db,
        payment_id=payment_id,
    )

    if payment is None:

        raise HTTPException(
            status_code=404,
            detail="Payment not found.",
        )

    return payment


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=201,
)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):

    return PaymentService.create_payment(
        db=db,
        payment_data=payment,
    )


@router.put(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def update_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
):

    updated_payment = PaymentService.update_payment(
        db=db,
        payment_id=payment_id,
        payment_data=payment,
    )

    if updated_payment is None:

        raise HTTPException(
            status_code=404,
            detail="Payment not found.",
        )

    return updated_payment


@router.delete(
    "/{payment_id}",
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):

    deleted = PaymentService.delete_payment(
        db=db,
        payment_id=payment_id,
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Payment not found.",
        )

    return {
        "message": "Payment deleted successfully.",
    }