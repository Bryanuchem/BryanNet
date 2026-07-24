from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy.orm import (
    relationship,
)

from sqlalchemy.sql import (
    func,
)

from app.database.base import (
    Base,
)

from app.database.sqlalchemy_enum import (
    sql_enum,
)

from app.enums.pending_login_status import (
    PendingLoginStatus,
)


class PendingLogin(Base):

    __tablename__ = "pending_logins"

    pending_login_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    login_token = Column(
        String(128),
        nullable=False,
        unique=True,
    )

    customer_id = Column(
        BigInteger,
        ForeignKey(
            "customers.customer_id",
        ),
        nullable=False,
    )

    router_id = Column(
        BigInteger,
        ForeignKey(
            "routers.router_id",
        ),
        nullable=False,
    )

    router_account_id = Column(
        BigInteger,
        ForeignKey(
            "router_accounts.router_account_id",
        ),
        nullable=False,
    )

    subscription_id = Column(
        BigInteger,
        ForeignKey(
            "subscriptions.subscription_id",
        ),
        nullable=False,
    )

    plan_id = Column(
        Integer,
        ForeignKey(
            "plans.plan_id",
        ),
        nullable=False,
    )

    device_mac = Column(
        String(50),
        nullable=False,
    )

    device_ip = Column(
        String(45),
        nullable=True,
    )

    device_id = Column(
        BigInteger,
        ForeignKey(
            "devices.device_id",
        ),
        nullable=True,
    )

    link_orig = Column(
        Text,
        nullable=True,
    )

    status = Column(
        sql_enum(
            PendingLoginStatus,
            name="pending_login_status",
        ),
        nullable=False,
        default=PendingLoginStatus.PENDING,
    )

    expires_at = Column(
        TIMESTAMP,
        nullable=False,
    )

    consumed_at = Column(
        TIMESTAMP,
        nullable=True,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    device = relationship(
        "Device",
        back_populates="pending_logins",
    )

    router_session = relationship(
        "RouterSession",
        back_populates="pending_login",
        uselist=False,
    )

    customer = relationship(
        "Customer",
        back_populates="pending_logins",
    )

    router = relationship(
        "Router",
        back_populates="pending_logins",
    )

    router_account = relationship(
        "RouterAccount",
        back_populates="pending_logins",
    )

    subscription = relationship(
        "Subscription",
        back_populates="pending_logins",
    )

    plan = relationship(
        "Plan",
        back_populates="pending_logins",
    )