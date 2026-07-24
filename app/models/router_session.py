from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    Enum,
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


class RouterSession(Base):

    __tablename__ = "router_sessions"

    router_session_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    router_account_id = Column(
        BigInteger,
        ForeignKey(
            "router_accounts.router_account_id",
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

    device_id = Column(
        BigInteger,
        ForeignKey(
            "devices.device_id",
        ),
        nullable=True,
    )

    pending_login_id = Column(
        BigInteger,
        ForeignKey(
            "pending_logins.pending_login_id",
        ),
        unique=True,
        nullable=True,
    )

    username = Column(
        String(100),
        nullable=False,
    )

    session_type = Column(
        Enum(
            "hotspot",
            "ppp",
            "dhcp",
            "vpn",
            name="router_session_type",
        ),
        nullable=False,
    )

    ip_address = Column(
        String(45),
        nullable=True,
    )

    mac_address = Column(
        String(50),
        nullable=True,
    )

    login_source = Column(
        String(50),
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

    bytes_in = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    bytes_out = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    packets_in = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    packets_out = Column(
        BigInteger,
        nullable=False,
        default=0,
    )

    disconnect_reason = Column(
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

    router_account = relationship(
        "RouterAccount",
        back_populates="router_sessions",
    )

    router = relationship(
        "Router",
        back_populates="router_sessions",
    )

    device = relationship(
        "Device",
        back_populates="router_sessions",
    )
    
    pending_login = relationship(
        "PendingLogin",
        back_populates="router_session",
    )
    
    portal_session = relationship(
        "PortalSession",
        back_populates="router_session",
        uselist=False,
    )