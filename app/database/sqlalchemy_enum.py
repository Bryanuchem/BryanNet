from sqlalchemy import Enum


def sql_enum(enum_class, name: str):
    """
    SQLAlchemy Enum that stores the enum values instead of the enum names.

    Example:
        CustomerStatus.ACTIVE -> "active"
        AdminRole.SUPER_ADMIN -> "super_admin"
    """

    return Enum(
        enum_class,
        values_callable=lambda enum: [member.value for member in enum],
        name=name,
    )