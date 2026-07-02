from datetime import datetime, UTC

from app.providers.notification.base import (
    BaseNotificationProvider,
)

from app.schemas.notification import (
    NotificationRequest,
    NotificationResponse,
)


class TelegramNotificationProvider(
    BaseNotificationProvider,
):

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _resolve_chat_id(
        recipient,
    ):

        if recipient is None:

            raise ValueError(
                "Recipient cannot be None."
            )

        chat_id = getattr(
            recipient,
            "telegram_chat_id",
            None,
        )

        if not chat_id:

            raise ValueError(
                "Recipient does not have a "
                "Telegram chat ID."
            )

        return chat_id

    @staticmethod
    def _send_to_telegram(
        chat_id,
        message,
    ):
        """
        Placeholder.

        Future implementation will delegate
        to the BryanNet Telegram bot.
        """

        #
        # Future
        #
        # TelegramBotService.send_message(
        #     chat_id=chat_id,
        #     text=message,
        # )
        #

        return {

            "success": True,

            "message_id":
                "telegram-placeholder",

        }

    # ==========================================================
    # Business Commands
    # ==========================================================

    def send(
        self,
        notification: NotificationRequest,
    ) -> NotificationResponse:

        chat_id = (
            self._resolve_chat_id(
                notification.recipient,
            )
        )

        result = (
            self._send_to_telegram(

                chat_id,

                notification.message,

            )
        )

        return NotificationResponse(

            success=result["success"],

            provider="telegram",

            recipient=str(chat_id),

            message_id=result.get(
                "message_id",
            ),

            detail=(
                "Notification sent."
            ),

            sent_at=datetime.now(UTC),

        )