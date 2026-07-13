from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    DECIMAL,
    String,
    TIMESTAMP,
    ForeignKey,
    Text,
)

from sqlalchemy import func

from sqlalchemy.orm import relationship

from app.database.base import Base

from app.enums import PaymentStatus

from app.database.sqlalchemy_enum import (
    sql_enum,
)

from app.enums.payment_provider import PaymentProvider

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

    payment_provider = Column(
        sql_enum(
            PaymentProvider, 
            "payment_provider"),
        nullable=False,
        default=PaymentProvider.MANUAL,
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
        sql_enum(
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
    
    transactions = relationship(
        "PaymentTransaction",
        back_populates="payment",
        cascade="all, delete-orphan",
        order_by="PaymentTransaction.created_at",
    )