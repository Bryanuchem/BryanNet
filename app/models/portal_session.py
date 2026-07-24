from sqlalchemy import (
    Column,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    TIMESTAMP,
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


class PortalSession(Base):

    __tablename__ = "portal_sessions"

    portal_session_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
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

    router_session_id = Column(
        BigInteger,
        ForeignKey(
            "router_sessions.router_session_id",
        ),
        nullable=False,
    )

    device_id = Column(
        BigInteger,
        ForeignKey(
            "devices.device_id",
        ),
        nullable=True,
    )

    login_at = Column(
        DateTime,
        nullable=False,
    )

    logout_at = Column(
        DateTime,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    termination_reason = Column(
        String(100),
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
        back_populates="portal_sessions",
    )

    router = relationship(
        "Router",
        back_populates="portal_sessions",
    )

    router_account = relationship(
        "RouterAccount",
        back_populates="portal_sessions",
    )

    router_session = relationship(
        "RouterSession",
        back_populates="portal_session",
    )

    device = relationship(
        "Device",
        back_populates="portal_sessions",
    )