from datetime import datetime
from datetime import timedelta

from sqlalchemy import func

from app.models.customer import Customer
from app.models.subscription import Subscription
from app.models.device import Device
from app.models.payment import Payment


class DashboardService:

    @staticmethod
    def get_summary(db):

        today = datetime.now().date()

        next_7_days = (
            datetime.now()
            + timedelta(days=7)
        )

        total_customers = (
            db.query(Customer)
            .count()
        )

        active_subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "active"
            )
            .count()
        )

        queued_subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "queued"
            )
            .count()
        )

        active_devices = (
            db.query(Device)
            .filter(
                Device.device_status == "active"
            )
            .count()
        )

        total_payments = (
            db.query(Payment)
            .filter(
                Payment.status == "successful"
            )
            .count()
        )

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.status == "successful"
            )
            .scalar()
        )

        revenue_today = (
            db.query(
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                )
            )
            .filter(
                Payment.status == "successful",
                func.date(
                    Payment.payment_date
                ) == today
            )
            .scalar()
        )

        expiring_today = (
            db.query(Subscription)
            .filter(
                Subscription.status == "active",
                func.date(
                    Subscription.expiry_date
                ) == today
            )
            .count()
        )

        expiring_next_7_days = (
            db.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.expiry_date >= datetime.now(),
                Subscription.expiry_date <= next_7_days
            )
            .count()
        )

        new_customers_today = (
            db.query(Customer)
            .filter(
                func.date(
                    Customer.created_at
                ) == today
            )
            .count()
        )

        new_customers_this_month = (
            db.query(Customer)
            .filter(
                func.month(
                    Customer.created_at
                ) == datetime.now().month,
                func.year(
                    Customer.created_at
                ) == datetime.now().year
            )
            .count()
        )

        return {
            "total_customers": total_customers,
            "active_subscriptions": active_subscriptions,
            "queued_subscriptions": queued_subscriptions,
            "active_devices": active_devices,

            "total_revenue": float(total_revenue),
            "total_payments": total_payments,

            "revenue_today": float(revenue_today),

            "expiring_today": expiring_today,
            "expiring_next_7_days": expiring_next_7_days,

            "new_customers_today": new_customers_today,
            "new_customers_this_month": new_customers_this_month
        }