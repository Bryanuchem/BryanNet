from uuid import uuid4

from app.models.payment import Payment


class PaymentService:

    @staticmethod
    def create_payment(
        db,
        customer_id,
        subscription_id,
        amount,
        payment_method="system"
    ):

        payment = Payment(
            customer_id=customer_id,
            subscription_id=subscription_id,
            amount=amount,
            payment_method=payment_method,
            payment_reference=str(uuid4()),
            status="successful"
        )

        db.add(payment)

        return payment