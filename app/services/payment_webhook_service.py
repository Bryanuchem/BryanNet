from fastapi import (
    HTTPException,
)

from app.services.payment_dispatcher_service import (
    PaymentDispatcherService,
)

from app.services.payment_transaction_service import (
    PaymentTransactionService,
)


class PaymentWebhookService:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def process_webhook(
        db,
        payment_provider,
        headers,
        body,
        payload,
    ):

        validation = (
            PaymentDispatcherService
            .validate_webhook(
                payment_provider=payment_provider,
                headers=headers,
                body=body,
            )
        )

        if not validation.valid:

            raise HTTPException(
                status_code=401,
                detail=(
                    "Invalid webhook signature."
                ),
            )

        webhook = (
            PaymentDispatcherService
            .parse_webhook(
                payment_provider=payment_provider,
                payload=payload,
            )
        )

        if not webhook.valid:

            return {
                "processed": False,
                "message": (
                    "Unsupported webhook."
                ),
            }

        transaction = (
            PaymentTransactionService
            .get_by_gateway_reference(
                db=db,
                gateway_reference=(
                    webhook.gateway_reference
                ),
            )
        )

        PaymentDispatcherService.verify_payment(
            db=db,
            transaction_id=(
                transaction.transaction_id
            ),
        )

        PaymentDispatcherService.complete_payment(
            db=db,
            transaction_id=(
                transaction.transaction_id
            ),
        )

        return {
            "processed": True,
        }