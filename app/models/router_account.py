from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    TIMESTAMP,
    Boolean,
    Integer,
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

    encrypted_password = Column(
        String(500),
        nullable=False,
    )

    profile_name = Column(
        String(100),
        nullable=True,
    )

    is_enabled = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    last_synchronized_at = Column(
        DateTime,
        nullable=True,
    )

    last_connected_at = Column(
        DateTime,
        nullable=True,
    )

    last_disconnected_at = Column(
        DateTime,
        nullable=True,
    )

    last_sync_status = Column(
        String(50),
        nullable=True,
    )

    last_sync_message = Column(
        String(500),
        nullable=True,
    )

    sync_attempts = Column(
        Integer,
        nullable=False,
        default=0,
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