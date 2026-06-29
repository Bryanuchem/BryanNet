from datetime import datetime

from sqlalchemy.orm import Session

from app.schemas.administration import (
    AdministrationMetrics,
    RecentAuditLogItem,
    ActiveSessionItem,
    SystemActivityItem,
    AdministrationOverviewResponse,
)


class AdministrationService:

    @staticmethod
    def get_overview(
        db: Session,
    ) -> AdministrationOverviewResponse:
        return AdministrationOverviewResponse(
            metrics=AdministrationMetrics(
                admin_users=12,
                active_sessions=4,
                roles=5,
                audit_events_today=186,
                system_events_today=923,
            ),
            recent_audit_logs=[
                RecentAuditLogItem(
                    id=1,
                    timestamp=datetime.now(),
                    administrator="Bryan",
                    action="Created",
                    module="Customers",
                    target="John Doe",
                    status="Success",
                ),
                RecentAuditLogItem(
                    id=2,
                    timestamp=datetime.now(),
                    administrator="Mary",
                    action="Updated",
                    module="Plans",
                    target="Premium 50",
                    status="Success",
                ),
                RecentAuditLogItem(
                    id=3,
                    timestamp=datetime.now(),
                    administrator="Bryan",
                    action="Suspended",
                    module="Subscriptions",
                    target="SUB-000245",
                    status="Success",
                ),
                RecentAuditLogItem(
                    id=4,
                    timestamp=datetime.now(),
                    administrator="System",
                    action="Backup",
                    module="Database",
                    target="Daily Backup",
                    status="Success",
                ),
                RecentAuditLogItem(
                    id=5,
                    timestamp=datetime.now(),
                    administrator="Admin",
                    action="Login",
                    module="Authentication",
                    target="Bryan",
                    status="Success",
                ),
            ],
            active_sessions=[
                ActiveSessionItem(
                    id=1,
                    administrator="Bryan",
                    device="Desktop",
                    browser="Chrome",
                    ip_address="192.168.1.101",
                    login_time=datetime.now(),
                    status="Active",
                ),
                ActiveSessionItem(
                    id=2,
                    administrator="Mary",
                    device="Laptop",
                    browser="Edge",
                    ip_address="192.168.1.102",
                    login_time=datetime.now(),
                    status="Active",
                ),
                ActiveSessionItem(
                    id=3,
                    administrator="John",
                    device="Mobile",
                    browser="Safari",
                    ip_address="192.168.1.103",
                    login_time=datetime.now(),
                    status="Idle",
                ),
                ActiveSessionItem(
                    id=4,
                    administrator="Support",
                    device="Desktop",
                    browser="Firefox",
                    ip_address="192.168.1.104",
                    login_time=datetime.now(),
                    status="Active",
                ),
            ],
            system_activity=[
                SystemActivityItem(
                    id=1,
                    timestamp=datetime.now(),
                    title="Payment verification completed",
                    description="Payment for subscription SUB-000245 was successfully verified.",
                ),
                SystemActivityItem(
                    id=2,
                    timestamp=datetime.now(),
                    title="Telegram notification sent",
                    description="Customer John Doe received a subscription activation notification.",
                ),
                SystemActivityItem(
                    id=3,
                    timestamp=datetime.now(),
                    title="Subscription activated",
                    description="Premium 50 plan activated successfully.",
                ),
                SystemActivityItem(
                    id=4,
                    timestamp=datetime.now(),
                    title="Scheduled backup completed",
                    description="Daily database backup finished successfully.",
                ),
                SystemActivityItem(
                    id=5,
                    timestamp=datetime.now(),
                    title="Router synchronization completed",
                    description="Router status synchronized with the platform.",
                ),
            ],
        )