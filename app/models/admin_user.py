from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    TIMESTAMP,
    Enum
)

from sqlalchemy.sql import func

from app.database.base import Base

from app.enums.admin_role import AdminRole


class AdminUser(Base):

    __tablename__ = "admin_users"

    admin_user_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(
            AdminRole,
            name="admin_role"
        ),
        nullable=False,
        default=AdminRole.SUPER_ADMIN
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )