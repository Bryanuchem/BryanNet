from abc import ABC
from abc import abstractmethod

from app.schemas.notification import (
    NotificationRequest,
    NotificationResponse,
)


class BaseNotificationProvider(
    ABC,
):

    @abstractmethod
    def send(
        self,
        notification: NotificationRequest,
    ) -> NotificationResponse:
        """
        Send a notification.
        """

        raise NotImplementedError