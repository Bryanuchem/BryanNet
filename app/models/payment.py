from sqlalchemy import (
    Column,
    BigInteger,
    DECIMAL,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.base import Base


class Payment(Base):

    __tablename__ = "payments"

    payment_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    subscription_id = Column(
        BigInteger,
        ForeignKey("subscriptions.subscription_id"),
        nullable=True
    )

    amount = Column(
        DECIMAL(12, 2),
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    payment_reference = Column(
        String(100),
        unique=True,
        nullable=False
    )

    status = Column(
        Enum(
            "pending",
            "successful",
            "failed",
            name="payment_status"
        ),
        default="successful"
    )

    payment_date = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )