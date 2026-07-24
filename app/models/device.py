from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    TIMESTAMP,
    Enum,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base

from app.enums import DeviceStatus

from app.database.sqlalchemy_enum import (
    sql_enum,
)

class Device(Base):

    __tablename__ = "devices"

    device_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    device_name = Column(
        String(100),
        nullable=True,
    )

    mac_address = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    device_type = Column(
        Enum(
            "phone",
            "laptop",
            "desktop",
            "tablet",
            "tv",
            "router",
            "unknown",
            name="device_type",
        ),
        nullable=False,
        default="unknown",
    )

    device_status = Column(
        sql_enum(
            DeviceStatus,
            name="device_status",
        ),
        nullable=False,
        default=DeviceStatus.ACTIVE,
    )

    online = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    approved_by_customer = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    first_seen = Column(
        DateTime,
        nullable=True,
    )

    last_seen = Column(
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
        back_populates="devices",
    )
    
    router_sessions = relationship(
        "RouterSession",
        back_populates="device",
    )
    
    portal_sessions = relationship(
        "PortalSession",
        back_populates="device",
    )
    
    pending_logins = relationship(
        "PendingLogin",
        back_populates="device",
    )