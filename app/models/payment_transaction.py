from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String,
    Text,
    TIMESTAMP,
)

from sqlalchemy.dialects.mysql import (
    JSON,
)

from sqlalchemy.orm import (
    relationship,
)

from sqlalchemy import func

from app.database.base import Base

from app.database.sqlalchemy_enum import (
    sql_enum,
)

from app.enums import (
    PaymentProvider,
)

from app.enums.transaction_status import (
    TransactionStatus,
)


class PaymentTransaction(Base):

    __tablename__ = "payment_transactions"

    transaction_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    payment_id = Column(
        BigInteger,
        ForeignKey(
            "payments.payment_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    payment_provider = Column(
        sql_enum(
            PaymentProvider,
            "payment_provider",
        ),
        nullable=False,
    )

    transaction_status = Column(
        sql_enum(
            TransactionStatus,
            "transaction_status",
        ),
        nullable=False,
        default=TransactionStatus.PENDING,
    )

    gateway_reference = Column(
        String(255),
        nullable=True,
    )

    gateway_transaction_id = Column(
        String(255),
        nullable=True,
    )

    gateway_status = Column(
        String(100),
        nullable=True,
    )

    authorization_code = Column(
        String(255),
        nullable=True,
    )

    currency = Column(
        String(3),
        nullable=False,
        default="NGN",
    )

    gateway_response = Column(
        Text,
        nullable=True,
    )

    gateway_metadata = Column(
        "metadata",
        JSON,
        nullable=True,
    )

    checkout_url = Column(
        Text,
        nullable=True,
    )

    access_code = Column(
        String(255),
        nullable=True,
    )

    paid_at = Column(
        TIMESTAMP,
        nullable=True,
    )

    webhook_received_at = Column(
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

    payment = relationship(
        "Payment",
        back_populates="transactions",
    )