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
    )

    mac_address = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    device_status = Column(
        Enum(
            "active",
            "blocked",
            "removed",
            name="device_status",
        ),
        default="active",
    )

    approved_by_customer = Column(
        Boolean,
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
    )

    customer = relationship(
        "Customer",
        back_populates="devices",
    )