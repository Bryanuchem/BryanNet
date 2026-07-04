from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base

from app.enums import RouterStatus

from app.database.sqlalchemy_enum import (
    sql_enum,
)

from app.enums import RouterProviderType

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

    router_type = Column(
        sql_enum(
            RouterProviderType,
            name="router_provider_type",
        ),
        nullable=False,
        default=RouterProviderType.SIMULATED,
    )

    status = Column(
        sql_enum(
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