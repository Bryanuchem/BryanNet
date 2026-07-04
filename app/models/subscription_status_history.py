from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP,
    Enum,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.base import Base


class SubscriptionStatusHistory(Base):

    __tablename__ = "subscription_status_history"

    history_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    subscription_id = Column(
        BigInteger,
        ForeignKey(
            "subscriptions.subscription_id"
        ),
        nullable=False
    )

    old_status = Column(
        Enum(
            "queued",
            "active",
            "expired",
            "suspended",
            "cancelled",
            name="history_old_status"
        ),
        nullable=True
    )

    new_status = Column(
        Enum(
            "queued",
            "active",
            "expired",
            "suspended",
            "cancelled",
            name="history_new_status"
        ),
        nullable=False
    )

    change_reason = Column(
        String(255)
    )

    changed_by_type = Column(
        Enum(
            "system",
            "customer",
            "admin",
            "agent",
            name="history_changed_by"
        ),
        default="system"
    )

    changed_by_id = Column(
        BigInteger,
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )