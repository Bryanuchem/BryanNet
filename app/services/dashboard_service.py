from datetime import datetime
from datetime import timedelta
import calendar

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
                    Payment.created_at

                    # Payment.payment_date

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

    @staticmethod
    def get_revenue_overview(
        db,
        period="month"
    ):

        today = datetime.now()

        # ======================================================
        # Last 7 Days
        # ======================================================

        if period == "7d":

            start_date = (
                today - timedelta(days=6)
            ).date()

            revenue = (
                db.query(
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    ).label("day"),
                    func.coalesce(
                        func.sum(Payment.amount),
                        0
                    ).label("revenue"),
                )
                .filter(
                    Payment.status == "successful",
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    ) >= start_date,
                )
                .group_by(
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    )
                )
                .all()
            )

            revenue_lookup = {
                row.day: float(row.revenue)
                for row in revenue
            }

            return [
                {
                    "label": day.strftime("%d %b"),
                    "revenue": revenue_lookup.get(
                        day,
                        0.0,
                    ),
                }
                for day in [
                    start_date + timedelta(days=i)
                    for i in range(7)
                ]
            ]

        # ======================================================
        # Last 30 Days
        # ======================================================

        if period == "30d":

            start_date = (
                today - timedelta(days=29)
            ).date()

            revenue = (
                db.query(
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    ).label("day"),
                    func.coalesce(
                        func.sum(Payment.amount),
                        0
                    ).label("revenue"),
                )
                .filter(
                    Payment.status == "successful",
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    ) >= start_date,
                )
                .group_by(
                    func.date(
                        Payment.created_at

                        # Payment.payment_date

                    )
                )
                .all()
            )

            revenue_lookup = {
                row.day: float(row.revenue)
                for row in revenue
            }

            return [
                {
                    "label": day.strftime("%d %b"),
                    "revenue": revenue_lookup.get(
                        day,
                        0.0,
                    ),
                }
                for day in [
                    start_date + timedelta(days=i)
                    for i in range(30)
                ]
            ]

        # ======================================================
        # Last 12 Months
        # ======================================================

        if period == "12m":

            current_year = today.year

            revenue = (
                db.query(
                    func.month(
                        Payment.created_at

                        # Payment.payment_date

                    ).label("month"),
                    func.coalesce(
                        func.sum(Payment.amount),
                        0
                    ).label("revenue"),
                )
                .filter(
                    Payment.status == "successful",
                    func.year(
                        Payment.created_at

                        # Payment.payment_date

                    ) == current_year,
                )
                .group_by(
                    func.month(
                        Payment.created_at

                        # Payment.payment_date

                    )
                )
                .order_by(
                    func.month(
                        Payment.created_at

                        # Payment.payment_date

                    )
                )
                .all()
            )

            revenue_lookup = {
                row.month: float(row.revenue)
                for row in revenue
            }

            return [
                {
                    "label": calendar.month_abbr[month],
                    "revenue": revenue_lookup.get(
                        month,
                        0.0,
                    ),
                }
                for month in range(1, 13)
            ]

        # ======================================================
        # This Month (Default)
        # ======================================================

        start_of_month = datetime(
            today.year,
            today.month,
            1,
        ).date()

        revenue = (
            db.query(
                func.date(
                    Payment.created_at

                    # Payment.payment_date

                ).label("day"),
                func.coalesce(
                    func.sum(Payment.amount),
                    0
                ).label("revenue"),
            )
            .filter(
                Payment.status == "successful",
                func.date(
                    Payment.created_at

                    # Payment.payment_date

                ) >= start_of_month,
            )
            .group_by(
                func.date(
                    Payment.created_at

                    # Payment.payment_date

                )
            )
            .all()
        )

        revenue_lookup = {
            row.day: float(row.revenue)
            for row in revenue
        }

        days_in_month = calendar.monthrange(
            today.year,
            today.month,
        )[1]

        return [
            {
                "label": f"{day}",
                "revenue": revenue_lookup.get(
                    datetime(
                        today.year,
                        today.month,
                        day,
                    ).date(),
                    0.0,
                ),
            }
            for day in range(
                1,
                days_in_month + 1,
            )
        ]
        
    @staticmethod
    def get_subscription_breakdown(
        db
    ):

        subscriptions = (
            db.query(
                Subscription.status,
                func.count(
                    Subscription.subscription_id
                ).label("count")
            )
            .group_by(
                Subscription.status
            )
            .all()
        )

        breakdown = {
            row.status.capitalize(): row.count
            for row in subscriptions
        }

        statuses = [
            "Active",
            "Queued",
            "Expired",
            "Cancelled",
        ]

        return [
            {
                "status": status,
                "count": breakdown.get(
                    status,
                    0,
                ),
            }
            for status in statuses
        ]        
        
    @staticmethod
    def get_recent_activity(
        db,
        limit=10,
    ):

        activities = []

        # ==========================
        # Customers
        # ==========================

        customers = (
            db.query(Customer)
            .order_by(
                Customer.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        for customer in customers:

            activities.append({
                "type": "customer",
                "title": "New customer registered",
                "description": customer.full_name,
                "created_at": customer.created_at,
            })

        # ==========================
        # Subscriptions
        # ==========================

        subscriptions = (
            db.query(Subscription)
            .order_by(
                Subscription.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        for subscription in subscriptions:

            activities.append({
                "type": "subscription",
                "title": "Subscription created",
                "description": subscription.status.capitalize(),
                "created_at": subscription.created_at,
            })

        # ==========================
        # Payments
        # ==========================

        payments = (
            db.query(Payment)
            .filter(
                Payment.status == "successful"
            )
            .order_by(
                Payment.created_at.desc()

                # Payment.payment_date.desc()

            )
            .limit(limit)
            .all()
        )

        for payment in payments:

            activities.append({
                "type": "payment",
                "title": "Payment received",
                "description": f"₦{payment.amount:,.0f}",
                "created_at": payment.created_at,

                # "created_at": payment.payment_date,
            })

        # ==========================
        # Devices
        # ==========================

        devices = (
            db.query(Device)
            .order_by(
                Device.created_at.desc()
            )
            .limit(limit)
            .all()
        )

        for device in devices:

            activities.append({
                "type": "device",
                "title": "Device registered",
                "description": device.device_name,
                "created_at": device.created_at,
            })

        activities.sort(
            key=lambda x: x["created_at"],
            reverse=True,
        )

        return activities[:limit]        