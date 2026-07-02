from app.providers.notification.base import (
    BaseNotificationProvider,
)

from app.schemas.notification import (
    NotificationRequest,
)


class SMSNotificationProvider(
    BaseNotificationProvider,
):

    def send(
        self,
        notification: NotificationRequest,
    ):

        raise NotImplementedError(
            "SMS notification provider "
            "has not been implemented."
        )