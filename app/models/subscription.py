from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database.base import Base

from app.enums import SubscriptionStatus

from app.database.sqlalchemy_enum import (
    sql_enum,
)

class Subscription(Base):

    __tablename__ = "subscriptions"

    subscription_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    plan_id = Column(
        Integer,
        ForeignKey("plans.plan_id"),
        nullable=False,
    )

    start_date = Column(
        DateTime,
        nullable=False,
    )

    expiry_date = Column(
        DateTime,
        nullable=False,
    )

    activated_at = Column(
        DateTime,
        nullable=True,
    )

    activation_sequence = Column(
        Integer,
        default=1,
        nullable=False,
    )

    status = Column(
        sql_enum(
            SubscriptionStatus,
            "subscription_status",
        ),
        nullable=False,
        default=SubscriptionStatus.QUEUED,
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

    customer = relationship(
        "Customer",
        back_populates="subscriptions",
    )

    plan = relationship(
        "Plan",
        back_populates="subscriptions",
    )

    payments = relationship(
        "Payment",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )
    
    pending_logins = relationship(
        "PendingLogin",
        back_populates="subscription",
    )