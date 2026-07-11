from io import BytesIO
from decimal import Decimal
from datetime import datetime

from fastapi import HTTPException

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.enums import PaymentStatus

from app.models.payment import Payment

from app.services.payment_service import (
    PaymentService,
)

COMPANY_NAME = "BryanNet ISP"

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
    def _format_currency(
        value,
    ):

        if value is None:

            return "-"

        return (
            f"₦{Decimal(value):,.2f}"
        )

    @staticmethod
    def _format_datetime(
        value,
    ):

        if value is None:

            return "-"

        if isinstance(
            value,
            datetime,
        ):

            return value.strftime(
                "%d %b %Y %H:%M",
            )

        return str(
            value,
        )

    @staticmethod
    def _format_date(
        value,
    ):

        if value is None:

            return "-"

        if isinstance(
            value,
            datetime,
        ):

            return value.strftime(
                "%d %b %Y",
            )

        return str(
            value,
        )

    @staticmethod
    def _format_enum(
        value,
    ):

        if value is None:

            return "-"

        if hasattr(
            value,
            "value",
        ):

            value = value.value

        return (
            str(value)
            .replace(
                "_",
                " ",
            )
            .title()
        )

    @staticmethod
    def _build_table(
        rows,
    ):

        table = Table(
            rows,
            colWidths=[
                2.2 * inch,
                4.1 * inch,
            ],
        )

        table.setStyle(

            TableStyle(

                [

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),

                    (
                        "LINEBELOW",
                        (0, -1),
                        (-1, -1),
                        0.25,
                        colors.lightgrey,
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold",
                    ),

                ]

            )

        )

        return table

    @staticmethod
    def _render_pdf(
        title,
        sections,
    ):

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            rightMargin=0.6 * inch,
            leftMargin=0.6 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch,
        )

        styles = getSampleStyleSheet()

        heading = styles["Heading1"]
        heading.alignment = TA_CENTER

        sub_heading = styles["Heading2"]

        normal = styles["BodyText"]

        story = [

            Paragraph(
                COMPANY_NAME,
                heading,
            ),

            Paragraph(
                title,
                sub_heading,
            ),

            Spacer(
                1,
                0.30 * inch,
            ),

        ]

        for section_title, rows in sections:

            story.append(

                Paragraph(
                    section_title,
                    sub_heading,
                )

            )

            story.append(
                Spacer(
                    1,
                    0.08 * inch,
                )
            )

            story.append(

                PaymentDocumentService
                ._build_table(
                    rows,
                )

            )

            story.append(

                Spacer(
                    1,
                    0.22 * inch,
                )

            )

        story.append(

            Paragraph(

                (
                    f"Thank you for choosing "
                    f"<b>{COMPANY_NAME}</b>."
                ),

                normal,

            )

        )

        story.append(

            Paragraph(

                (
                    "This receipt serves as proof "
                    "of payment."
                ),

                normal,

            )

        )

        story.append(

            Paragraph(

                (
                    "Generated: "
                    f"{datetime.utcnow().strftime('%d %b %Y %H:%M UTC')}"
                ),

                normal,

            )

        )

        story.append(

            Paragraph(

                (
                    f"&copy; {COMPANY_NAME}"
                ),

                normal,

            )

        )

        document.build(
            story,
        )

        buffer.seek(
            0,
        )

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

        sections = [

            (

                "Receipt Information",

                [

                    (

                        "Receipt Number",

                        payment.payment_reference,

                    ),

                    (

                        "Payment Reference",

                        payment.payment_reference,

                    ),

                    (

                        "Gateway Reference",

                        (
                            payment.gateway_transaction_id
                            or "-"
                        ),

                    ),

                ],

            ),

            (

                "Customer",

                [

                    (

                        "Customer Name",

                        customer.full_name,

                    ),

                    (

                        "Phone Number",

                        customer.phone_number,

                    ),

                ],

            ),

            (

                "Subscription",

                [

                    (

                        "Plan",

                        plan.plan_name,

                    ),

                    (

                        "Speed",

                        (
                            f"{plan.speed_limit_mbps} Mbps"
                        ),

                    ),

                    (

                        "Start Date",

                        PaymentDocumentService
                        ._format_date(

                            subscription.start_date
                            if subscription
                            else None

                        ),

                    ),

                    (

                        "Expiry Date",

                        PaymentDocumentService
                        ._format_date(

                            subscription.expiry_date
                            if subscription
                            else None

                        ),

                    ),

                ],

            ),

            (

                "Payment",

                [

                    (

                        "Amount",

                        PaymentDocumentService
                        ._format_currency(
                            payment.amount,
                        ),

                    ),

                    (

                        "Provider",

                        PaymentDocumentService
                        ._format_enum(
                            payment.payment_provider,
                        ),

                    ),

                    (

                        "Channel",

                        PaymentDocumentService
                        ._format_enum(
                            payment.payment_channel,
                        ),

                    ),

                    (

                        "Method",

                        payment.payment_method
                        or "-",

                    ),

                    (

                        "Status",

                        PaymentDocumentService
                        ._format_enum(
                            payment.status,
                        ),

                    ),

                    (

                        "Paid At",

                        PaymentDocumentService
                        ._format_datetime(
                            payment.payment_date,
                        ),

                    ),

                ],

            ),

        ]

        return (

            PaymentDocumentService
            ._render_pdf(

                "PAYMENT RECEIPT",

                sections,

            )

        )

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

        sections = [

            (

                "Invoice Information",

                [

                    (

                        "Invoice Number",

                        payment.payment_reference,

                    ),

                    (

                        "Payment Reference",

                        payment.payment_reference,

                    ),

                    (

                        "Generated",

                        PaymentDocumentService
                        ._format_datetime(
                            payment.created_at,
                        ),

                    ),

                ],

            ),

            (

                "Customer",

                [

                    (

                        "Customer Name",

                        customer.full_name,

                    ),

                    (

                        "Phone Number",

                        customer.phone_number,

                    ),

                ],

            ),

            (

                "Subscription",

                [

                    (

                        "Plan",

                        plan.plan_name,

                    ),

                    (

                        "Speed",

                        (
                            f"{plan.speed_limit_mbps} Mbps"
                        ),

                    ),

                    (

                        "Start Date",

                        PaymentDocumentService
                        ._format_date(

                            subscription.start_date
                            if subscription
                            else None

                        ),

                    ),

                    (

                        "Expiry Date",

                        PaymentDocumentService
                        ._format_date(

                            subscription.expiry_date
                            if subscription
                            else None

                        ),

                    ),

                ],

            ),

            (

                "Payment",

                [

                    (

                        "Amount",

                        PaymentDocumentService
                        ._format_currency(
                            payment.amount,
                        ),

                    ),

                    (

                        "Provider",

                        PaymentDocumentService
                        ._format_enum(
                            payment.payment_provider,
                        ),

                    ),

                    (

                        "Channel",

                        PaymentDocumentService
                        ._format_enum(
                            payment.payment_channel,
                        ),

                    ),

                    (

                        "Method",

                        payment.payment_method
                        or "-",

                    ),

                    (

                        "Status",

                        PaymentDocumentService
                        ._format_enum(
                            payment.status,
                        ),

                    ),

                ],

            ),

        ]

        return (

            PaymentDocumentService
            ._render_pdf(

                "PAYMENT INVOICE",

                sections,

            )

        )

    # ==========================================================
    # PDF Generation
    # ==========================================================

    @staticmethod
    def generate_receipt_pdf(
        db,
        payment_reference,
    ):

        return (

            PaymentDocumentService
            .generate_receipt(

                db,

                payment_reference,

            )

        )

    @staticmethod
    def generate_invoice_pdf(
        db,
        payment_reference,
    ):

        return (

            PaymentDocumentService
            .generate_invoice(

                db,

                payment_reference,

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

            db.query(
                Payment,
            )

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

            db.query(
                Payment,
            )

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