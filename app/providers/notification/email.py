from app.providers.notification.base import (
    BaseNotificationProvider,
)

from app.schemas.notification import (
    NotificationRequest,
)


class EmailNotificationProvider(
    BaseNotificationProvider,
):

    def send(
        self,
        notification: NotificationRequest,
    ):

        raise NotImplementedError(
            "Email notification provider "
            "has not been implemented."
        )