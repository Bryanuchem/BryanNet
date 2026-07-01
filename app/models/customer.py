from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    Boolean,
    TIMESTAMP,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database.base import Base
from app.enums.next_action import NextAction

from app.enums import CustomerStatus

class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    phone_number = Column(
        String(20),
        unique=True,
        nullable=True,
    )

    full_name = Column(
        String(150),
        nullable=True,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True,
    )

    whatsapp_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    status = Column(
        Enum(
            CustomerStatus,
            name="customer_status",
        ),
        nullable=False,
        default=CustomerStatus.ACTIVE,
    )

    referred_by_agent_id = Column(
        BigInteger,
        # ForeignKey("agents.agent_id"),
        nullable=True,
    )

    telegram_user_id = Column(
        BigInteger,
        unique=True,
        nullable=True,
    )

    is_registered = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    registration_step = Column(
        Enum(
            NextAction,
            name="customer_registration_step",
        ),
        nullable=False,
        default=NextAction.START_ONBOARDING,
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
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    devices = relationship(
        "Device",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    
    router_accounts = relationship(
        "RouterAccount",
        back_populates="customer",
        cascade="all, delete-orphan",
    )    