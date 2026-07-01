from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DECIMAL,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey,
    Text,
)

from sqlalchemy import func

from sqlalchemy.orm import relationship

from app.database.base import Base

from app.enums import PaymentStatus


class Payment(Base):

    __tablename__ = "payments"

    payment_id = Column(
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

    subscription_id = Column(
        BigInteger,
        ForeignKey("subscriptions.subscription_id"),
        nullable=True,
    )

    amount = Column(
        DECIMAL(12, 2),
        nullable=False,
    )

    payment_channel = Column(
        String(50),
        nullable=False,
    )

    payment_method = Column(
        String(100),
        nullable=True,
    )

    payment_reference = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    gateway_transaction_id = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    status = Column(
        Enum(
            PaymentStatus,
            name="payment_status",
        ),
        nullable=False,
        default=PaymentStatus.PENDING,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    payment_date = Column(
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

    customer = relationship(
        "Customer",
        back_populates="payments",
    )

    plan = relationship(
        "Plan",
        back_populates="payments",
    )

    subscription = relationship(
        "Subscription",
        back_populates="payments",
    )