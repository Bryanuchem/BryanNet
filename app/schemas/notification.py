from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.enums import (
    NotificationCategory,
    NotificationPriority,
)


class NotificationRequest(
    BaseModel,
):

    recipient: Any

    subject: str

    message: str

    priority: NotificationPriority = (
        NotificationPriority.NORMAL
    )

    category: NotificationCategory = (
        NotificationCategory.CUSTOMER
    )

    metadata: dict[str, Any] | None = None


class NotificationResponse(
    BaseModel,
):

    success: bool

    provider: str

    recipient: str

    message_id: str | None = None

    detail: str | None = None

    sent_at: datetime | None = None


class NotificationResult(
    BaseModel,
):

    notification: NotificationRequest

    response: NotificationResponse