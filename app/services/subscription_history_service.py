from app.models.subscription_status_history import (
    SubscriptionStatusHistory
)


class SubscriptionHistoryService:

    @staticmethod
    def log_status_change(
        db,
        subscription_id,
        old_status,
        new_status,
        reason,
        changed_by_type="system",
        changed_by_id=None
    ):

        history = SubscriptionStatusHistory(
            subscription_id=subscription_id,
            old_status=old_status,
            new_status=new_status,
            change_reason=reason,
            changed_by_type=changed_by_type,
            changed_by_id=changed_by_id
        )

        db.add(history)

        db.commit()

        db.refresh(history)

        return history
    