from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DateTime,
    Enum,
    TIMESTAMP,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.base import Base


class Subscription(Base):

    __tablename__ = "subscriptions"

    subscription_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    plan_id = Column(
        Integer,
        ForeignKey("plans.plan_id"),
        nullable=False
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    expiry_date = Column(
        DateTime,
        nullable=False
    )

    activation_sequence = Column(
        Integer,
        default=1
    )

    status = Column(
        Enum(
            "queued",
            "active",
            "expired",
            "suspended",
            "cancelled",
            name="subscription_status"
        ),
        default="queued"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )