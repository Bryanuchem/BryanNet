from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Integer,
    Boolean,
    Float,
    DateTime,
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

    hostname = Column(
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

    api_port = Column(
        Integer,
        nullable=False,
        default=8728,
    )

    api_username = Column(
        String(100),
        nullable=False,
    )

    encrypted_api_password = Column(
        String(500),
        nullable=False,
    )

    use_ssl = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    connection_timeout = Column(
        Integer,
        nullable=False,
        default=10,
    )

    last_health_check = Column(
    DateTime,
    nullable=True,
)

    last_latency_ms = Column(
        Float,
        nullable=True,
    )

    router_os_version = Column(
        String(100),
        nullable=True,
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