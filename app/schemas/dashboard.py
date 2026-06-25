from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_customers: int
    active_subscriptions: int
    queued_subscriptions: int
    active_devices: int

    total_revenue: float
    total_payments: int

    revenue_today: float

    expiring_today: int
    expiring_next_7_days: int

    new_customers_today: int
    new_customers_this_month: int