from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.enums import (
    PaymentProvider,
)

from app.services.payment_webhook_service import (
    PaymentWebhookService,
)

router = APIRouter(
    prefix="/payments/webhooks",
    tags=["Payment Webhooks"],
)


# ==========================================================
# Paystack
# ==========================================================

@router.post(
    "/paystack",
)
async def paystack_webhook(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
):

    raw_body = await request.body()

    payload = await request.json()

    headers = dict(
        request.headers,
    )

    PaymentWebhookService.process_webhook(

        db=db,

        payment_provider=(
            PaymentProvider.PAYSTACK
        ),

        headers=headers,

        body=raw_body,

        payload=payload,

    )

    return {
        "processed": True,
    }