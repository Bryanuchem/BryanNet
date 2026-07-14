from fastapi import (
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.domain import (
    RouterContext,
)

from app.models.customer import (
    Customer,
)

from app.models.device import (
    Device,
)

from app.models.plan import (
    Plan,
)

from app.models.router import (
    Router,
)

from app.models.router_account import (
    RouterAccount,
)

from app.models.subscription import (
    Subscription,
)

from app.services.router_credential_manager import (
    RouterCredentialManager,
)


class RouterContextService:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _get_router_account(
        db: Session,
        router_account_id: int,
    ):

        router_account = (

            db.query(

                RouterAccount,

            )

            .filter(

                RouterAccount.router_account_id
                == router_account_id,

            )

            .first()

        )

        if router_account is None:

            raise HTTPException(

                status_code=404,

                detail=(

                    "Router account not found."

                ),

            )

        return router_account

    @staticmethod
    def _decrypt_password(
        router_account: RouterAccount,
    ):

        encrypted_password = str(

            router_account.encrypted_password

        )

        if not encrypted_password:

            raise HTTPException(

                status_code=400,

                detail=(

                    "Router account password "

                    "is not configured."

                ),

            )

        return (

            RouterCredentialManager.decrypt(

                encrypted_password,

            )

        )

    # ==========================================================
    # Context Builder
    # ==========================================================

    @staticmethod
    def from_router_account(
        db: Session,
        router_account_id: int,
    ):

        router_account = (

            RouterContextService

            ._get_router_account(

                db,

                router_account_id,

            )

        )

        subscription = (

            db.query(

                Subscription,

            )

            .filter(

                Subscription.subscription_id
                == router_account.subscription_id,

            )

            .first()

        )

        if subscription is None:

            raise HTTPException(

                status_code=404,

                detail="Subscription not found.",

            )

        customer = (

            db.query(

                Customer,

            )

            .filter(

                Customer.customer_id
                == subscription.customer_id,

            )

            .first()

        )

        if customer is None:

            raise HTTPException(

                status_code=404,

                detail="Customer not found.",

            )

        plan = (

            db.query(

                Plan,

            )

            .filter(

                Plan.plan_id
                == subscription.plan_id,

            )

            .first()

        )

        if plan is None:

            raise HTTPException(

                status_code=404,

                detail="Plan not found.",

            )

        router = (

            db.query(

                Router,

            )

            .filter(

                Router.router_id
                == router_account.router_id,

            )

            .first()

        )

        if router is None:

            raise HTTPException(

                status_code=404,

                detail="Router not found.",

            )

        devices = (

            db.query(

                Device,

            )

            .filter(

                Device.customer_id
                == customer.customer_id,

            )

            .all()

        )

        return RouterContext(

            customer=customer,

            subscription=subscription,

            plan=plan,

            router=router,

            router_account=router_account,

            plaintext_password=(

                RouterContextService

                ._decrypt_password(

                    router_account,

                )

            ),

            devices=devices,

        )