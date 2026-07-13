from datetime import datetime, UTC
from typing import Any, cast

from fastapi import HTTPException

from app.enums import (
    PaymentProvider,
    TransactionStatus,
)

from app.models.payment import Payment
from app.models.payment_transaction import (
    PaymentTransaction,
)


class PaymentTransactionService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_transaction(
        db,
        transaction_id,
    ):

        transaction = (

            db.query(
                PaymentTransaction,
            )

            .filter(
                PaymentTransaction.transaction_id
                == transaction_id,
            )

            .first()

        )

        if not transaction:

            raise HTTPException(
                status_code=404,
                detail="Transaction not found.",
            )

        return transaction

    @staticmethod
    def _find_latest_transaction(
        db,
        payment_id,
    ):

        return (

            db.query(
                PaymentTransaction,
            )

            .filter(
                PaymentTransaction.payment_id
                == payment_id,
            )

            .order_by(
                PaymentTransaction.created_at.desc(),
            )

            .first()

        )

    @staticmethod
    def _find_payment(
        db,
        payment_id,
    ):

        payment = (

            db.query(
                Payment,
            )

            .filter(
                Payment.payment_id
                == payment_id,
            )

            .first()

        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found.",
            )

        return payment

    @staticmethod
    def _validate_retry_allowed(
        payment,
    ):

        if payment.status.value != "PENDING":

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only pending payments "
                    "can create new transactions."
                ),
            )

    @staticmethod
    def _mark_pending(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.PENDING
        )

    @staticmethod
    def _mark_successful(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.SUCCESSFUL
        )

    @staticmethod
    def _mark_failed(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.FAILED
        )

    @staticmethod
    def _mark_cancelled(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.CANCELLED
        )

    @staticmethod
    def _mark_expired(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.EXPIRED
        )

    @staticmethod
    def _mark_abandoned(
        transaction,
    ):

        transaction.transaction_status = (
            TransactionStatus.ABANDONED
        )

    @staticmethod
    def _create_transaction(
        db,
        payment_id,
        payment_provider,
    ):

        transaction = PaymentTransaction(

            payment_id=payment_id,

            payment_provider=payment_provider,

            transaction_status=(
                TransactionStatus.PENDING
            ),

        )

        db.add(
            transaction,
        )

        db.commit()

        db.refresh(
            transaction,
        )

        return transaction

    @staticmethod
    def _finalize(
        db,
        transaction,
    ):

        db.commit()

        db.refresh(
            transaction,
        )

        return transaction

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def get_or_create_transaction(
        db,
        payment_id,
        payment_provider: PaymentProvider,
    ):

        transaction = (

            PaymentTransactionService
            .get_latest_transaction(
                db,
                payment_id,
            )

        )

        if (

            transaction

            and

            transaction.transaction_status
            == TransactionStatus.PENDING

        ):

            return transaction

        return (

            PaymentTransactionService
            .create_transaction(

                db=db,

                payment_id=payment_id,

                payment_provider=(
                    payment_provider
                ),

            )

        )

    @staticmethod
    def create_transaction(
        db,
        payment_id,
        payment_provider: PaymentProvider,
    ):

        PaymentTransactionService._find_payment(
            db,
            payment_id,
        )

        return (

            PaymentTransactionService
            ._create_transaction(

                db,

                payment_id,

                payment_provider,

            )

        )

    @staticmethod
    def create_retry_transaction(
        db,
        payment_id,
        payment_provider: PaymentProvider,
    ):

        payment = (

            PaymentTransactionService
            ._find_payment(
                db,
                payment_id,
            )

        )

        PaymentTransactionService \
            ._validate_retry_allowed(
                payment,
            )

        return (

            PaymentTransactionService
            ._create_transaction(

                db,

                payment_id,

                payment_provider,

            )

        )

    @staticmethod
    def record_initialization(
        db,
        transaction_id,
        gateway_reference=None,
        gateway_status=None,
        gateway_response=None,
        metadata=None,
    ):

        transaction = (

            PaymentTransactionService
            ._find_transaction(
                db,
                transaction_id,
            )

        )

        transaction.gateway_reference = (
            gateway_reference
        )

        transaction.gateway_status = (
            gateway_status
        )

        transaction.gateway_response = (
            gateway_response
        )

        transaction.gateway_metadata = metadata

        return (

            PaymentTransactionService
            ._finalize(
                db,
                transaction,
            )

        )

    @staticmethod
    def record_verification(
        db,
        transaction_id,
        transaction_status,
        gateway_transaction_id=None,
        authorization_code=None,
        paid_at=None,
        gateway_status=None,
        gateway_response=None,
        metadata=None,
    ):

        transaction = (

            PaymentTransactionService
            ._find_transaction(
                db,
                transaction_id,
            )

        )

        if (
            transaction_status
            == TransactionStatus.PENDING
        ):

            PaymentTransactionService \
                ._mark_pending(
                    transaction,
                )

        elif (
            transaction_status
            == TransactionStatus.SUCCESSFUL
        ):

            PaymentTransactionService \
                ._mark_successful(
                    transaction,
                )

        elif (
            transaction_status
            == TransactionStatus.FAILED
        ):

            PaymentTransactionService \
                ._mark_failed(
                    transaction,
                )

        elif (
            transaction_status
            == TransactionStatus.CANCELLED
        ):

            PaymentTransactionService \
                ._mark_cancelled(
                    transaction,
                )

        elif (
            transaction_status
            == TransactionStatus.EXPIRED
        ):

            PaymentTransactionService \
                ._mark_expired(
                    transaction,
                )

        elif (
            transaction_status
            == TransactionStatus.ABANDONED
        ):

            PaymentTransactionService \
                ._mark_abandoned(
                    transaction,
                )

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported transaction status."
                ),
            )

        transaction.gateway_transaction_id = (
            gateway_transaction_id
        )

        transaction.authorization_code = (
            authorization_code
        )

        transaction.paid_at = paid_at

        transaction.gateway_status = (
            gateway_status
        )

        transaction.gateway_response = (
            gateway_response
        )

        transaction.gateway_metadata = metadata

        return (

            PaymentTransactionService
            ._finalize(
                db,
                transaction,
            )

        )
        
    @staticmethod
    def record_webhook(
        db,
        transaction_id,
        metadata=None,
    ):

        transaction = (

            PaymentTransactionService
            ._find_transaction(
                db,
                transaction_id,
            )

        )

        transaction.webhook_received_at = (
            datetime.now(
                UTC,
            )
        )

        transaction.metadata = metadata

        return (

            PaymentTransactionService
            ._finalize(
                db,
                transaction,
            )

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_transaction(
        db,
        transaction_id,
    ):

        return (

            PaymentTransactionService
            ._find_transaction(
                db,
                transaction_id,
            )

        )

    @staticmethod
    def get_latest_transaction(
        db,
        payment_id,
    ):

        return (

            PaymentTransactionService
            ._find_latest_transaction(
                db,
                payment_id,
            )

        )

    @staticmethod
    def get_payment_transactions(
        db,
        payment_id,
    ):

        return (

            db.query(
                PaymentTransaction,
            )

            .filter(
                PaymentTransaction.payment_id
                == payment_id,
            )

            .order_by(
                PaymentTransaction.created_at,
            )

            .all()

        )

    @staticmethod
    def get_transaction_by_gateway_reference(
        db,
        gateway_reference,
    ):

        transaction = (

            db.query(
                PaymentTransaction,
            )

            .filter(
                PaymentTransaction.gateway_reference
                == gateway_reference,
            )

            .first()

        )

        if not transaction:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Transaction not found."
                ),
            )

        return transaction