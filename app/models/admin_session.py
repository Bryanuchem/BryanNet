from sqlalchemy import (
    Column,
    BigInteger,
    Boolean,
    DateTime,
    TIMESTAMP,
    Text,
    String,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class AdminSession(Base):

    __tablename__ = "admin_sessions"

    admin_session_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    admin_user_id = Column(
        BigInteger,
        ForeignKey("admin_users.admin_user_id"),
        nullable=False,
    )

    login_time = Column(
        DateTime,
        nullable=False,
        index=True,
    )

    last_activity = Column(
        DateTime,
        nullable=False,
    )

    logout_time = Column(
        DateTime,
        nullable=True,
    )

    ip_address = Column(
        String(45),
        nullable=True,
    )

    user_agent = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    admin_user = relationship(
        "AdminUser",
        back_populates="admin_sessions",
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="admin_session",
    )