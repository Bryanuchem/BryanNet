from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    TIMESTAMP,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class Permission(Base):

    __tablename__ = "permissions"

    permission_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    permission_key = Column(
        String(150),
        unique=True,
        nullable=False,
    )

    module = Column(
        String(100),
        nullable=False,
    )

    action = Column(
        String(100),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
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

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan",
    )