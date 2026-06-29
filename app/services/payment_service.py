from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    func,
    or_,
)

from app.models.customer import Customer
from app.models.payment import Payment


class PaymentService:

    @staticmethod
    def get_payment_summary(
        db,
    ):

        total_revenue = (

            db.query(

                func.coalesce(
                    func.sum(
                        Payment.amount,
                    ),
                    0,
                ),

            )

            .filter(
                Payment.status == "successful",
            )

            .scalar()

        )

        total_payments = (

            db.query(
                func.count(
                    Payment.payment_id,
                ),
            )

            .scalar()

        )

        successful_payments = (

            db.query(
                func.count(
                    Payment.payment_id,
                ),
            )

            .filter(
                Payment.status == "successful",
            )

            .scalar()

        )

        pending_payments = (

            db.query(
                func.count(
                    Payment.payment_id,
                ),
            )

            .filter(
                Payment.status == "pending",
            )

            .scalar()

        )

        failed_payments = (

            db.query(
                func.count(
                    Payment.payment_id,
                ),
            )

            .filter(
                Payment.status == "failed",
            )

            .scalar()

        )

        return {

            "total_payments":
                total_payments,

            "total_revenue":
                total_revenue,

            "successful_payments":
                successful_payments,

            "pending_payments":
                pending_payments,

            "failed_payments":
                failed_payments,

        }

    @staticmethod
    def get_all_payments(
        db,
        search=None,
        payment_channel=None,
        status=None,
    ):

        query = (

            db.query(

                Payment,

                Customer.full_name.label(
                    "customer_name",
                ),

                Customer.phone_number.label(
                    "phone_number",
                ),

            )

            .join(

                Customer,

                Payment.customer_id
                == Customer.customer_id,

            )

        )

        if search:

            query = query.filter(

                or_(

                    Customer.full_name.ilike(
                        f"%{search}%"
                    ),

                    Customer.phone_number.ilike(
                        f"%{search}%"
                    ),

                    Payment.payment_reference.ilike(
                        f"%{search}%"
                    ),

                )

            )

        if payment_channel:

            query = query.filter(

                Payment.payment_channel
                == payment_channel

            )

        if status:

            query = query.filter(

                Payment.status
                == status

            )

        results = (

            query.order_by(

                Payment.created_at.desc()

            )

            .all()

        )

        return [

            {

                "payment_id":
                    payment.payment_id,

                "customer_id":
                    payment.customer_id,

                "customer_name":
                    customer_name,

                "phone_number":
                    phone_number,

                "subscription_id":
                    payment.subscription_id,

                "amount":
                    payment.amount,

                "payment_channel":
                    payment.payment_channel,

                "payment_method":
                    payment.payment_method,

                "payment_reference":
                    payment.payment_reference,

                "status":
                    payment.status,

                "notes":
                    payment.notes,

                "payment_date":
                    payment.payment_date,

                "created_at":
                    payment.created_at,

                "updated_at":
                    payment.updated_at,

            }

            for (

                payment,
                customer_name,
                phone_number,

            ) in results

        ]

    @staticmethod
    def get_payment(
        db,
        payment_id,
    ):

        result = (

            db.query(

                Payment,

                Customer.full_name.label(
                    "customer_name",
                ),

                Customer.phone_number.label(
                    "phone_number",
                ),

            )

            .join(

                Customer,

                Payment.customer_id
                == Customer.customer_id,

            )

            .filter(

                Payment.payment_id
                == payment_id

            )

            .first()

        )

        if result is None:

            return None

        payment, customer_name, phone_number = result

        return {

            "payment_id":
                payment.payment_id,

            "customer_id":
                payment.customer_id,

            "customer_name":
                customer_name,

            "phone_number":
                phone_number,

            "subscription_id":
                payment.subscription_id,

            "amount":
                payment.amount,

            "payment_channel":
                payment.payment_channel,

            "payment_method":
                payment.payment_method,

            "payment_reference":
                payment.payment_reference,

            "status":
                payment.status,

            "notes":
                payment.notes,

            "payment_date":
                payment.payment_date,

            "created_at":
                payment.created_at,

            "updated_at":
                payment.updated_at,

        }

    @staticmethod
    def create_payment(
        db,
        payment_data,
    ):

        payment = Payment(

            customer_id=payment_data.customer_id,

            subscription_id=payment_data.subscription_id,

            amount=payment_data.amount,

            payment_channel=payment_data.payment_channel,

            payment_method=payment_data.payment_method,

            payment_reference=f"PAY-{uuid4().hex[:12].upper()}",

            status=payment_data.status,

            notes=payment_data.notes,

            payment_date=(

                payment_data.payment_date

                or datetime.utcnow()

            ),

        )

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return PaymentService.get_payment(

            db,

            payment.payment_id,

        )

    @staticmethod
    def update_payment(
        db,
        payment_id,
        payment_data,
    ):

        payment = (

            db.query(Payment)

            .filter(

                Payment.payment_id
                == payment_id

            )

            .first()

        )

        if payment is None:

            return None

        payment.customer_id = (
            payment_data.customer_id
        )

        payment.subscription_id = (
            payment_data.subscription_id
        )

        payment.amount = (
            payment_data.amount
        )

        payment.payment_channel = (
            payment_data.payment_channel
        )

        payment.payment_method = (
            payment_data.payment_method
        )

        payment.status = (
            payment_data.status
        )

        payment.notes = (
            payment_data.notes
        )

        payment.payment_date = (

            payment_data.payment_date

            or payment.payment_date

        )

        db.commit()

        db.refresh(payment)

        return PaymentService.get_payment(

            db,

            payment.payment_id,

        )

    @staticmethod
    def delete_payment(
        db,
        payment_id,
    ):

        payment = (

            db.query(Payment)

            .filter(

                Payment.payment_id
                == payment_id

            )

            .first()

        )

        if payment is None:

            return False

        db.delete(payment)

        db.commit()

        return True