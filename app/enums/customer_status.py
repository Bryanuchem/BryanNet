from enum import Enum


class CustomerStatus(str, Enum):

    ACTIVE = "active"

    SUSPENDED = "suspended"

    BLOCKED = "blocked"