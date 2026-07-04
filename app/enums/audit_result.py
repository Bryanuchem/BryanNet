from enum import Enum


class AuditResult(str, Enum):

    SUCCESS = "SUCCESS"

    WARNING = "WARNING"

    FAILED = "FAILED"

    INFO = "INFO"