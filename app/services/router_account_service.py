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
            .assign_router(

                db,

                customer_id,

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