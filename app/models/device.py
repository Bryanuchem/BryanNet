from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base

from app.enums import DeviceStatus

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
        Enum(
            DeviceStatus,
            name="device_status",
        ),
        nullable=False,
        default=DeviceStatus.ACTIVE,
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