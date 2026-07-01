from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class RouterAccount(Base):

    __tablename__ = "router_accounts"

    router_account_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    router_id = Column(
        BigInteger,
        ForeignKey("routers.router_id"),
        nullable=False,
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    profile_name = Column(
        String(100),
        nullable=True,
    )

    status = Column(
        Enum(
            "active",
            "suspended",
            "expired",
            name="router_account_status",
        ),
        nullable=False,
        default="active",
    )

    last_sync_at = Column(
        DateTime,
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
        back_populates="router_accounts",
    )

    router = relationship(
        "Router",
        back_populates="router_accounts",
    )