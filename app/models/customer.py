from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    Boolean,
    TIMESTAMP,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database.base import Base


class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    phone_number = Column(
        String(20),
        unique=True,
        nullable=True
    )

    full_name = Column(
        String(150),
        nullable=True
    )

    whatsapp_enabled = Column(
        Boolean,
        default=True
    )

    status = Column(
        Enum(
            "active",
            "suspended",
            "blocked",
            name="customer_status"
        ),
        default="active"
    )

    referred_by_agent_id = Column(
        BigInteger,
       #ForeignKey("agents.agent_id"),
        nullable=True
    )

    telegram_user_id = Column(
        BigInteger,
        unique=True,
        nullable=True
    )
    is_registered = Column(
        Boolean,
        default=False,
        nullable=False
    )

    registration_step = Column(
        String(30),
        nullable=False,
        default="START"
    )    
    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

