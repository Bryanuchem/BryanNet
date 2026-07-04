from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Boolean,
    Enum,
    TIMESTAMP,
)

from sqlalchemy.sql import func

from app.database.base import Base


class Setting(Base):

    __tablename__ = "settings"

    setting_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    key = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    value = Column(
        Text,
        nullable=False,
    )

    value_type = Column(
        Enum(
            "string",
            "number",
            "boolean",
            "json",
            name="setting_value_type",
        ),
        nullable=False,
        default="string",
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_editable = Column(
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