from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    JSON,
    TIMESTAMP,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database.base import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    audit_log_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    admin_id = Column(
        BigInteger,
        ForeignKey("admin_users.admin_user_id"),
        nullable=False,
    )

    admin_session_id = Column(
        BigInteger,
        ForeignKey("admin_sessions.admin_session_id"),
        nullable=True,
    )

    action = Column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_type = Column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_id = Column(
        BigInteger,
        nullable=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    old_values = Column(
        JSON,
        nullable=True,
    )

    new_values = Column(
        JSON,
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

    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    admin_user = relationship(
        "AdminUser",
        back_populates="audit_logs",
    )

    admin_session = relationship(
        "AdminSession",
        back_populates="audit_logs",
    )