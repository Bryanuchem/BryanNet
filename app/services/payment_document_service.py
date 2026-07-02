from io import BytesIO

from fastapi import HTTPException

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from app.enums import PaymentStatus

from app.models.payment import Payment

from app.services.payment_service import (
    PaymentService,
)


class PaymentDocumentService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_payment(
        db,
        payment_reference,
    ):

        return (
            PaymentService.get_payment(
                db,
                payment_reference,
            )
        )

    @staticmethod
    def _validate_successful_payment(
        payment,
    ):

        if (
            payment.status
            != PaymentStatus.SUCCESSFUL
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Payment must be successful "
                    "before documents can be "
                    "generated."
                ),
            )

    @staticmethod
    def _render_pdf(
        title,
        document,
    ):

        buffer = BytesIO()

        pdf = canvas.Canvas(
            buffer,
        )

        y = 10.5 * inch

        pdf.setFont(
            "Helvetica-Bold",
            18,
        )

        pdf.drawString(
            inch,
            y,
            f"BryanNet ISP - {title}",
        )

        y -= 0.5 * inch

        pdf.setFont(
            "Helvetica",
            11,
        )

        for key, value in document.items():

            pdf.drawString(

                inch,

                y,

                (
                    f"{key.replace('_', ' ').title()}: "
                    f"{value}"
                ),

            )

            y -= 0.3 * inch

        pdf.save()

        buffer.seek(0)

        return buffer

    # ==========================================================
    # Document Generation
    # ==========================================================

    @staticmethod
    def generate_receipt(
        db,
        payment_reference,
    ):

        payment = (
            PaymentDocumentService
            ._find_payment(
                db,
                payment_reference,
            )
        )

        PaymentDocumentService._validate_successful_payment(
            payment,
        )

        customer = payment.customer

        plan = payment.plan

        subscription = (
            payment.subscription
        )

        return {

            "receipt_number":
                payment.payment_reference,

            "payment_reference":
                payment.payment_reference,

            "customer_name":
                customer.full_name,

            "phone_number":
                customer.phone_number,

            "plan_name":
                plan.plan_name,

            "speed":
                plan.speed_limit_mbps,

            "payment_provider":
                payment.payment_provider,

            "payment_method":
                payment.payment_method,

            "amount":
                payment.amount,

            "paid_at":
                payment.payment_date,

            "subscription_start":
                (
                    subscription.start_date
                    if subscription
                    else None
                ),

            "subscription_end":
                (
                    subscription.end_date
                    if subscription
                    else None
                ),

            "status":
                payment.status,

        }

    @staticmethod
    def generate_invoice(
        db,
        payment_reference,
    ):

        payment = (
            PaymentDocumentService
            ._find_payment(
                db,
                payment_reference,
            )
        )

        customer = payment.customer

        plan = payment.plan

        subscription = (
            payment.subscription
        )

        return {

            "invoice_number":
                payment.payment_reference,

            "payment_reference":
                payment.payment_reference,

            "customer_name":
                customer.full_name,

            "phone_number":
                customer.phone_number,

            "plan_name":
                plan.plan_name,

            "speed":
                plan.speed_limit_mbps,

            "payment_provider":
                payment.payment_provider,

            "payment_method":
                payment.payment_method,

            "amount":
                payment.amount,

            "generated_at":
                payment.created_at,

            "subscription_start":
                (
                    subscription.start_date
                    if subscription
                    else None
                ),

            "subscription_end":
                (
                    subscription.end_date
                    if subscription
                    else None
                ),

            "payment_status":
                payment.status,

        }
        
    # ==========================================================
    # PDF Generation
    # ==========================================================

    @staticmethod
    def generate_receipt_pdf(
        db,
        payment_reference,
    ):

        receipt = (
            PaymentDocumentService
            .generate_receipt(
                db,
                payment_reference,
            )
        )

        return (
            PaymentDocumentService
            ._render_pdf(
                "Receipt",
                receipt,
            )
        )

    @staticmethod
    def generate_invoice_pdf(
        db,
        payment_reference,
    ):

        invoice = (
            PaymentDocumentService
            .generate_invoice(
                db,
                payment_reference,
            )
        )

        return (
            PaymentDocumentService
            ._render_pdf(
                "Invoice",
                invoice,
            )
        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_payment_history(
        db,
        customer_id,
    ):

        return (

            db.query(Payment)

            .filter(
                Payment.customer_id
                == customer_id,
            )

            .order_by(
                Payment.payment_date.desc(),
            )

            .all()

        )

    @staticmethod
    def get_renewal_history(
        db,
        customer_id,
    ):

        return (

            db.query(Payment)

            .filter(

                Payment.customer_id
                == customer_id,

                Payment.status
                == PaymentStatus.SUCCESSFUL,

            )

            .order_by(
                Payment.payment_date.desc(),
            )

            .all()

        )       