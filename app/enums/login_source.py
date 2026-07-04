from enum import Enum


class LoginSource(str, Enum):

    WEB = "WEB"

    TELEGRAM = "TELEGRAM"

    API = "API"