from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Boolean,
    TIMESTAMP
)

from sqlalchemy.sql import func

from app.database.base import Base


class Plan(Base):

    __tablename__ = "plans"

    plan_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    plan_name = Column(
        String(50),
        nullable=False
    )

    price = Column(
        DECIMAL(10, 2),
        nullable=False
    )

    duration_days = Column(
        Integer,
        nullable=False
    )

    speed_limit_mbps = Column(
        Integer,
        nullable=False
    )

    max_devices = Column(
        Integer,
        nullable=False
    )

    concurrent_devices = Column(
        Integer,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )