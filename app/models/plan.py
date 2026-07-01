from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Boolean,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class Plan(Base):

    __tablename__ = "plans"

    plan_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    plan_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    description = Column(
        String(255),
        nullable=True,
    )

    price = Column(
        DECIMAL(12, 2),
        nullable=False,
    )

    duration_days = Column(
        Integer,
        nullable=False,
    )

    speed_limit_mbps = Column(
        Integer,
        nullable=False,
    )

    max_devices = Column(
        Integer,
        nullable=False,
        default=1,
    )

    concurrent_devices = Column(
        Integer,
        nullable=False,
        default=1,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
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

    subscriptions = relationship(
        "Subscription",
        back_populates="plan",
        cascade="all, delete-orphan",
    )