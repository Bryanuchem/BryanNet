from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    TIMESTAMP,
)

from sqlalchemy.sql import func

from app.database.base import Base

from sqlalchemy.orm import relationship

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
        nullable=True,
    )

    router_type = Column(
        Enum(
            "simulator",
            "mikrotik_chr",
            "mikrotik_physical",
            name="router_type",
        ),
        nullable=False,
        default="simulator",
    )

    status = Column(
        Enum(
            "online",
            "offline",
            "maintenance",
            name="router_status",
        ),
        nullable=False,
        default="online",
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