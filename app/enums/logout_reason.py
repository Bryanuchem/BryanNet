from enum import Enum


class LogoutReason(str, Enum):

    MANUAL = "MANUAL"

    CLOSE_ALL = "CLOSE_ALL"

    NEW_LOGIN = "NEW_LOGIN"

    TOKEN_EXPIRED = "TOKEN_EXPIRED"