from datetime import datetime

from pydantic import BaseModel

from app.enums.pending_login_status import (
    PendingLoginStatus,
)


class PendingLoginCreateSchema(BaseModel):

    login_token: str

    customer_id: int

    router_id: int

    router_account_id: int

    subscription_id: int

    plan_id: int

    device_mac: str

    device_ip: str | None = None

    link_orig: str | None = None

    expires_at: datetime


class PendingLoginConsumeSchema(BaseModel):

    login_token: str


class PendingLoginSchema(BaseModel):

    pending_login_id: int

    login_token: str

    customer_id: int

    router_id: int

    router_account_id: int

    subscription_id: int

    plan_id: int

    device_mac: str

    device_ip: str | None

    link_orig: str | None

    status: PendingLoginStatus

    expires_at: datetime

    consumed_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True