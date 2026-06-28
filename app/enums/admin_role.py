from enum import Enum


class AdminRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    FINANCE = "FINANCE"
    TECHNICIAN = "TECHNICIAN"