from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class VirtualRouterAccount(Base):

    __tablename__ = "virtual_router_accounts"

    virtual_router_account_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    router_id = Column(
        BigInteger,
        ForeignKey("routers.router_id"),
        nullable=False,
    )

    router_account_id = Column(
        BigInteger,
        ForeignKey(
            "router_accounts.router_account_id"
        ),
        nullable=False,
        unique=True,
    )

    username = Column(
        String(100),
        nullable=False,
    )

    enabled = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    connected = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    speed_limit_mbps = Column(
        Integer,
        nullable=False,
    )

    max_devices = Column(
        Integer,
        nullable=False,
    )

    concurrent_devices = Column(
        Integer,
        nullable=False,
    )

    approved_device_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_synchronized_at = Column(
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

    router = relationship(
        "Router",
    )

    router_account = relationship(
        "RouterAccount",
    )