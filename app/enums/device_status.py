from enum import Enum


class DeviceStatus(str, Enum):

    ACTIVE = "active"

    INACTIVE = "inactive"

    BLOCKED = "blocked"