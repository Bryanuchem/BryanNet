from datetime import datetime

from fastapi import HTTPException

from app.models.router_account import (
    RouterAccount,
)

from app.services.customer_service import (
    CustomerService,
)

from app.services.router_assignment_service import (
    RouterAssignmentService,
)

from app.services.router_credential_manager import (
    RouterCredentialManager,
)


from app.core.settings import (
    settings,
)

from app.models.subscription import (
    Subscription,
)

from app.enums import (
    SubscriptionStatus,
)

from app.utils.phone import(
    local_nigerian_phone_number,
)

class RouterAccountService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _find_account(
        db,
        router_account_id,
    ):

        account = (
            db.query(RouterAccount)
            .filter(
                RouterAccount.router_account_id
                == router_account_id
            )
            .first()
        )

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Router account not found.",
            )

        return account

    @staticmethod
    def _find_customer_account(
        db,
        customer_id,
        router_id,
    ):

        return (
            db.query(RouterAccount)
            .filter(
                RouterAccount.customer_id == customer_id,
                RouterAccount.router_id == router_id,
            )
            .first()
        )

    @staticmethod
    def _find_customer_default_account(
        db,
        customer_id,
    ):

        return (

            db.query(
                RouterAccount,
            )

            .filter(

                RouterAccount.customer_id
                == customer_id,

                RouterAccount.is_enabled.is_(True),

            )

            .order_by(

                RouterAccount.router_account_id.desc(),

            )

            .first()

        )

    @staticmethod
    def _find_username_account(
        db,
        username,
    ):

        return (

            db.query(
                RouterAccount,
            )

            .filter(

                RouterAccount.username
                == username,

            )

            .first()

        )

    @staticmethod
    def _generate_router_username(
        customer,
    ):

        if customer.phone_number:

            return (

                f"{settings.router_username_prefix}"

                f"{local_nigerian_phone_number(

                    customer.phone_number,

                )}"

            )

        return (
            f"CUST{customer.customer_id:06d}"
        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def ensure_router_account(
        db,
        customer_id,
    ):

        customer = (
            CustomerService.get_customer(
                db,
                customer_id,
            )
        )

        router = (

            RouterAssignmentService

            .select_router(

                db,

            )

        )

        existing_account = (

            RouterAccountService
            ._find_customer_account(

                db,

                customer_id,

                router.router_id,

            )

        )

        if existing_account:

            return existing_account

        password = (

            RouterCredentialManager
            .generate_password()

        )

        encrypted_password = (

            RouterCredentialManager
            .encrypt(
                password,
            )

        )

        account = RouterAccount(

            customer_id=customer_id,

            router_id=router.router_id,

            username=(

                RouterAccountService
                ._generate_router_username(
                    customer,
                )

            ),

            encrypted_password=encrypted_password,

            is_enabled=False,

        )

        db.add(
            account,
        )

        db.commit()

        db.refresh(
            account,
        )

        return account
    
    @staticmethod
    def provision_active_accounts(
        db,
    ):

        subscriptions = (

            db.query(

                Subscription,

            )

            .filter(

                Subscription.status
                == SubscriptionStatus.ACTIVE,

            )

            .order_by(

                Subscription.subscription_id,

            )

            .all()

        )

        processed = 0

        created = 0

        existing = 0

        for subscription in subscriptions:

            processed += 1

            router = (

                RouterAssignmentService

                .assign_router(

                    db,

                    subscription.customer_id,

                )

            )

            account = (

                RouterAccountService

                ._find_customer_account(

                    db,

                    subscription.customer_id,

                    router.router_id,

                )

            )

            if account:

                existing += 1

                continue

            RouterAccountService.ensure_router_account(

                db,

                subscription.customer_id,

            )

            created += 1

        return {

            "processed": processed,

            "created": created,

            "existing": existing,

        }

    @staticmethod
    def activate_account(
        db,
        router_account_id,
    ):

        account = (
            RouterAccountService
            ._find_account(
                db,
                router_account_id,
            )
        )

        account.is_enabled = True

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def mark_connected(
        db,
        router_account_id,
        message="Customer connected.",
    ):

        account = (

            RouterAccountService

            ._find_account(

                db,

                router_account_id,

            )

        )

        account.last_connected_at = (

            datetime.now()

        )

        account.last_sync_status = (
            "online"
        )

        account.last_sync_message = (
            message
        )

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def mark_disconnected(
        db,
        router_account_id,
        message="Customer disconnected.",
    ):

        account = (

            RouterAccountService

            ._find_account(

                db,

                router_account_id,

            )

        )

        account.last_disconnected_at = (

            datetime.now()

        )

        account.last_sync_status = (
            "offline"
        )

        account.last_sync_message = (
            message
        )

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def mark_sync_success(
        db,
        router_account_id,
        message="Synchronization successful.",
    ):

        account = (

            RouterAccountService

            ._find_account(

                db,

                router_account_id,

            )

        )

        account.last_synchronized_at = (

            datetime.now()

        )

        account.last_sync_status = (
            "success"
        )

        account.last_sync_message = (
            message
        )

        account.sync_attempts = 0

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def mark_sync_failed(
        db,
        router_account_id,
        message,
    ):

        account = (

            RouterAccountService

            ._find_account(

                db,

                router_account_id,

            )

        )

        account.last_synchronized_at = (

            datetime.now()

        )

        account.last_sync_status = (
            "failed"
        )

        account.last_sync_message = (
            message
        )

        account.sync_attempts += 1

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def suspend_account(
        db,
        router_account_id,
    ):

        account = (
            RouterAccountService
            ._find_account(
                db,
                router_account_id,
            )
        )

        account.is_enabled = False

        db.commit()

        db.refresh(
            account,
        )

        return account

    @staticmethod
    def remove_account(
        db,
        router_account_id,
    ):

        account = (
            RouterAccountService
            ._find_account(
                db,
                router_account_id,
            )
        )

        db.delete(
            account,
        )

        db.commit()

        return {
            "message":
                "Router account removed successfully."
        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_account(
        db,
        router_account_id,
    ):

        return (

            RouterAccountService
            ._find_account(

                db,

                router_account_id,

            )

        )

    @staticmethod
    def get_customer_account(
        db,
        customer_id,
        router_id,
    ):

        account = (

            RouterAccountService
            ._find_customer_account(

                db,

                customer_id,

                router_id,

            )

        )

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Router account not found.",
            )

        return account

    @staticmethod
    def get_customer_default_account(
        db,
        customer_id,
    ):

        account = (

            RouterAccountService

            ._find_customer_default_account(

                db,

                customer_id,

            )

        )

        if not account:

            raise HTTPException(

                status_code=404,

                detail=(
                    "No active router account found."
                ),

            )

        return account

    @staticmethod
    def get_username_account(
        db,
        username,
    ):

        account = (

            RouterAccountService

            ._find_username_account(

                db,

                username,

            )

        )

        if not account:

            raise HTTPException(

                status_code=404,

                detail=(
                    "Router account not found."
                ),

            )

        return account

    @staticmethod
    def get_router_accounts(
        db,
        router_id,
    ):

        return (

            db.query(
                RouterAccount,
            )

            .filter(
                RouterAccount.router_id == router_id,
            )

            .order_by(
                RouterAccount.router_account_id,
            )

            .all()

        )

    @staticmethod
    def get_all_accounts(
        db,
    ):

        return (

            db.query(
                RouterAccount,
            )

            .order_by(
                RouterAccount.router_account_id,
            )

            .all()

        )    