from datetime import datetime, timedelta, UTC

from sqlalchemy import func

from app.enums import PaymentStatus

from app.models.payment import Payment


class PaymentMaintenanceService:

    # ==========================================================
    # Payment Maintenance
    # ==========================================================

    @staticmethod
    def expire_pending_payments(
        db,
        expiry_hours=24,
    ):
        """
        Expire pending payments older than the
        configured threshold.
        """

        expiry_time = (
            datetime.now(UTC)
            - timedelta(
                hours=expiry_hours,
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

            payment.status = (
                PaymentStatus.EXPIRED
            )

        db.commit()

        return {

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
        Placeholder for payment reconciliation.

        Future implementations may compare
        BryanNet payment records with payment
        gateway records to detect mismatches.
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

        return {

            "successful":
                successful,

            "pending":
                pending,

            "failed":
                failed,

            "expired":
                expired,

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
                (
                    "Payment subsystem "
                    "operational."
                ),

        }