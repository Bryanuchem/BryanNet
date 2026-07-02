import secrets
import string

from fastapi import HTTPException

from app.domain import RouterContext

from app.models.router_account import RouterAccount

from app.services.customer_service import CustomerService
from app.services.device_service import DeviceService
from app.services.plan_service import PlanService
from app.services.router_service import RouterService
from app.services.subscription_service import (
    SubscriptionService,
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
    def _generate_username(
        customer,
    ):

        if customer.phone_number:

            return (
                f"BRN{customer.phone_number}"
            )

        return (
            f"CUST{customer.customer_id:06d}"
        )

    @staticmethod
    def _generate_password():

        alphabet = (
            string.ascii_letters
            + string.digits
        )

        return "".join(

            secrets.choice(alphabet)

            for _ in range(12)

        )

    @staticmethod
    def _validate_router(
        db,
        router_id,
    ):

        return (
            RouterService.get_router(
                db,
                router_id,
            )
        )

    # ==========================================================
    # Context Builder
    # ==========================================================

    @staticmethod
    def build_router_context(
        db,
        customer_id,
    ):

        customer = (
            CustomerService.get_customer(
                db,
                customer_id,
            )
        )

        subscription = (
            SubscriptionService
            .get_active_subscription(
                db,
                customer_id,
            )
        )

        if not subscription:

            raise HTTPException(
                status_code=400,
                detail="Customer has no active subscription.",
            )

        plan = (
            PlanService.get_plan(
                db,
                subscription.plan_id,
            )
        )

        router_account = (
            db.query(RouterAccount)
            .filter(
                RouterAccount.customer_id == customer_id,
            )
            .first()
        )

        if not router_account:

            raise HTTPException(
                status_code=404,
                detail="Router account not found.",
            )

        router = (
            RouterService.get_router(
                db,
                router_account.router_id,
            )
        )

        devices = (
            DeviceService.get_active_devices(
                db,
                customer_id,
            )
        )

        return RouterContext(

            customer=customer,

            subscription=subscription,

            plan=plan,

            router=router,

            router_account=router_account,

            devices=devices,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create_router_account(
        db,
        customer_id,
        router_id,
    ):

        customer = (
            CustomerService.get_customer(
                db,
                customer_id,
            )
        )

        RouterAccountService._validate_router(
            db,
            router_id,
        )

        existing_account = (

            RouterAccountService
            ._find_customer_account(

                db,

                customer_id,

                router_id,

            )

        )

        if existing_account:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Customer already has a "
                    "router account on this router."
                ),
            )

        account = RouterAccount(

            customer_id=customer_id,

            router_id=router_id,

            username=(

                RouterAccountService
                ._generate_username(
                    customer,
                )

            ),

            password=(

                RouterAccountService
                ._generate_password()

            ),

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

    @staticmethod
    def synchronize_customer_access(
        db,
        customer_id,
    ):

        context = (

            RouterAccountService
            .build_router_context(

                db,

                customer_id,

            )

        )

        return (

            RouterService
            .synchronize_customer(

                db,

                context,

            )

        )

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