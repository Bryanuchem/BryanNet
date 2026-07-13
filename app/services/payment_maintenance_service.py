from datetime import (
    datetime,
    timedelta,
    UTC,
)

from sqlalchemy import (
    func,
)

from app.services.audit_log_service import (
    AuditLogService,
)

from app.constants.audit_actions import (
    AUTOMATION_PAYMENTS,
)

from app.services.payment_service import (
    PaymentService,
)

from app.services.payment_dispatcher_service import (
    PaymentDispatcherService,
)

from app.services.payment_transaction_service import (
    PaymentTransactionService,
)

from app.core.settings import (
    settings,
)

from app.enums import (
    PaymentStatus,
    TransactionStatus,
)

from app.models.payment import (
    Payment,
)


class PaymentMaintenanceService:

    # ==========================================================
    # Payment Maintenance
    # ==========================================================

    @staticmethod
    def verify_pending_payments(
        db,
    ):
        """
        Retry verification for pending payments
        whose gateway transactions are still
        unresolved.
        """

        pending_payments = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.PENDING,

            )

            .all()

        )

        processed = 0

        verified = 0

        failed = 0

        skipped = 0

        for payment in pending_payments:

            transaction = (

                PaymentTransactionService
                .get_latest_transaction(

                    db,

                    payment.payment_id,

                )

            )

            if transaction is None:

                skipped += 1

                continue

            processed += 1

            try:

                result = (

                    PaymentDispatcherService
                    .verify_payment(

                        db,

                        transaction.transaction_id,

                    )

                )

                if result.verified:

                    PaymentDispatcherService.complete_payment(

                        db,

                        transaction.transaction_id,

                    )

                    verified += 1

                else:

                    failed += 1

            except Exception:

                failed += 1

        db.commit()

        return {

            "processed": processed,

            "verified": verified,

            "failed": failed,

            "skipped": skipped,

        }

    @staticmethod
    def expire_pending_payments(
        db,
    ):
        """
        Expire pending payments older than the
        configured threshold.
        """

        expiry_time = (

            datetime.now(UTC)

            - timedelta(

                hours=settings.payment_expiry_hours,

            )

        )

        expired_payments = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.PENDING,

                Payment.created_at
                <= expiry_time,

            )

            .all()

        )

        for payment in expired_payments:

            PaymentService._mark_expired(
                payment,
            )

        db.commit()

        return {

            "processed":
                len(expired_payments),

            "expired_payments":
                len(expired_payments),

        }

    @staticmethod
    def cleanup_stale_payments(
        db,
        stale_days=90,
    ):
        """
        Locate stale payments for future
        archival or cleanup.

        No records are deleted.
        """

        stale_date = (

            datetime.now(UTC)

            - timedelta(
                days=stale_days,
            )

        )

        stale_payments = (

            db.query(Payment)

            .filter(

                Payment.created_at
                <= stale_date,

            )

            .order_by(

                Payment.created_at,

            )

            .all()

        )

        return {

            "stale_payments":
                stale_payments,

            "count":
                len(stale_payments),

        }

    @staticmethod
    def reconcile_payments(
        db,
    ):
        """
        Summarize payment state for
        reconciliation reporting.
        """

        successful = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.SUCCESSFUL,

            )

            .count()

        )

        pending = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.PENDING,

            )

            .count()

        )

        failed = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.FAILED,

            )

            .count()

        )

        expired = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.EXPIRED,

            )

            .count()

        )

        refunded = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.REFUNDED,

            )

            .count()

        )

        cancelled = (

            db.query(Payment)

            .filter(

                Payment.status
                == PaymentStatus.CANCELLED,

            )

            .count()

        )

        return {

            "successful":
                successful,

            "pending":
                pending,

            "failed":
                failed,

            "expired":
                expired,

            "refunded":
                refunded,

            "cancelled":
                cancelled,

            "status":
                "Reconciliation complete.",

        }
        
    @staticmethod
    def payment_health_check(
        db,
    ):
        """
        Basic payment subsystem health.

        Future versions may include gateway
        connectivity and credential validation.
        """

        total_payments = (

            db.query(

                func.count(
                    Payment.payment_id,
                )

            )

            .scalar()

        )

        return {

            "healthy": True,

            "total_payments":
                total_payments,

            "message":

                "Payment subsystem operational.",

        }

    @staticmethod
    def run(
        db,
        admin=None,
        session=None,
    ):

        verification = (

            PaymentMaintenanceService

            .verify_pending_payments(

                db,

            )

        )

        expiration = (

            PaymentMaintenanceService

            .expire_pending_payments(

                db,

            )

        )

        reconciliation = (

            PaymentMaintenanceService

            .reconcile_payments(

                db,

            )

        )

        result = {

            "processed": (

                verification["processed"]

                + expiration["processed"]

            ),

            "verified":
                verification["verified"],

            "failed":
                verification["failed"],

            "skipped":
                verification["skipped"],

            "expired_payments":
                expiration["expired_payments"],

            "reconciliation":
                reconciliation,

        }

        AuditLogService.log_system_action(

            db=db,

            admin=admin,

            session=session,

            action=AUTOMATION_PAYMENTS,

            description=(

                "Payment maintenance completed. "

                f"Verified {result['verified']} payment(s), "

                f"expired {result['expired_payments']} payment(s), "

                f"failed {verification['failed']} verification(s), "

                f"skipped {verification['skipped']} payment(s)."

            ),

            entity_type="System",

            target_name="Payments",

            new_values={

                "processed":
                    result["processed"],

                "verified":
                    result["verified"],

                "failed":
                    verification["failed"],

                "skipped":
                    verification["skipped"],

                "expired_payments":
                    result["expired_payments"],

                "reconciliation":
                    result["reconciliation"],

            },

        )

        db.commit()

        return result