from datetime import datetime

from pydantic import BaseModel


class AdministrationMetrics(BaseModel):
    admin_users: int
    login_sessions_today: int
    roles: int
    audit_events_today: int
    system_events_today: int


class RecentAuditLogItem(BaseModel):
    id: int
    timestamp: datetime
    administrator: str
    action: str
    module: str
    target: str
    status: str


class ActiveSessionItem(BaseModel):
    id: int
    administrator: str
    device: str
    browser: str
    ip_address: str
    login_time: datetime
    status: str


class SystemActivityItem(BaseModel):
    id: int
    timestamp: datetime
    administrator: str
    action: str
    module: str
    target: str
    status: str


class AdministrationOverviewResponse(BaseModel):
    metrics: AdministrationMetrics
    recent_audit_logs: list[RecentAuditLogItem]
    active_sessions: list[ActiveSessionItem]
    system_activity: list[SystemActivityItem]