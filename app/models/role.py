from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Boolean,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class Role(Base):

    __tablename__ = "roles"

    role_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    role_name = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_system_role = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
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

    admin_users = relationship(
        "AdminUser",
        back_populates="role",
    )