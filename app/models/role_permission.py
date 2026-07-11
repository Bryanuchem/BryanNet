from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class RolePermission(Base):

    __tablename__ = "role_permissions"

    role_permission_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    role_id = Column(
        BigInteger,
        ForeignKey("roles.role_id"),
        nullable=False,
    )

    permission_id = Column(
        BigInteger,
        ForeignKey("permissions.permission_id"),
        nullable=False,
    )

    role = relationship(
        "Role",
        back_populates="role_permissions",
    )

    permission = relationship(
        "Permission",
        back_populates="role_permissions",
    )