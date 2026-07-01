from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base

from app.enums import RouterStatus

class Router(Base):

    __tablename__ = "routers"

    router_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    router_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    location_name = Column(
        String(200),
        nullable=True,
    )

    management_ip = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    api_username = Column(
        String(100),
        nullable=False,
    )

    api_password = Column(
        String(255),
        nullable=False,
    )

    status = Column(
        Enum(
            RouterStatus,
            name="router_status",
        ),
        nullable=False,
        default=RouterStatus.ONLINE,
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

    router_accounts = relationship(
        "RouterAccount",
        back_populates="router",
    )