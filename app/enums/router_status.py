from enum import Enum


class RouterStatus(str, Enum):

    ONLINE = "online"

    OFFLINE = "offline"

    MAINTENANCE = "maintenance"