from datetime import (
    datetime,
    timedelta,
    timezone,
)

from secrets import (
    token_urlsafe,
)

from sqlalchemy.orm import (
    Session,
)

from app.models.customer import (
    Customer,
)

from app.models.pending_login import (
    PendingLogin,
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

from app.enums.pending_login_status import (
    PendingLoginStatus,
)

from app.models.device import (
    Device,
)

class PendingLoginService:

    """
    Preserves BryanNet authentication context
    across the RouterOS hotspot handoff.

    Responsibilities

    - Create pending login records
    - Retrieve pending logins
    - Validate pending logins
    - Consume pending logins
    - Expire stale pending logins

    This service deliberately does NOT:

    - Authenticate customers
    - Create PortalSession
    - Create RouterSession
    - Register devices
    - Render templates
    - Call RouterOS
    """

    DEFAULT_EXPIRY_MINUTES = 5

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _generate_token() -> str:

        return token_urlsafe(
            32,
        )

    @staticmethod
    def _find_by_token(
        db: Session,
        token: str,
    ) -> PendingLogin:

        if not token:

            raise ValueError(
                "Login token is required."
            )

        pending_login = (

            db.query(
                PendingLogin,
            )

            .filter(
                PendingLogin.login_token == token,
            )

            .first()

        )

        if not pending_login:

            raise ValueError(
                "Pending login not found."
            )

        return pending_login

    @staticmethod
    def _validate_pending_login(
        pending_login: PendingLogin,
    ) -> None:

        if (
            pending_login.status
            != PendingLoginStatus.PENDING
        ):

            raise ValueError(
                "Pending login is no longer valid."
            )

        if PendingLoginService._is_expired(
            pending_login,
        ):

            raise ValueError(
                "Pending login has expired."
            )

    @staticmethod
    def _is_expired(
        pending_login: PendingLogin,
    ) -> bool:

        return (

            pending_login.expires_at

            <

            datetime.now()

        )

    # ==========================================================
    # Public API
    # ==========================================================

    @staticmethod
    def create(
        db: Session,
        *,
        customer: Customer,
        router: Router,
        router_account: RouterAccount,
        subscription: Subscription,
        plan: Plan,
        device: Device | None = None,
        device_mac: str,
        device_ip: str | None = None,
        link_orig: str | None = None,
    ) -> PendingLogin:

        if not customer:

            raise ValueError(
                "Customer is required."
            )

        if not router:

            raise ValueError(
                "Router is required."
            )

        if not router_account:

            raise ValueError(
                "Router account is required."
            )

        if not subscription:

            raise ValueError(
                "Subscription is required."
            )

        if not plan:

            raise ValueError(
                "Plan is required."
            )

        if not device_mac:

            raise ValueError(
                "Device MAC address is required."
            )

        pending_login = PendingLogin(

            login_token=PendingLoginService._generate_token(),

            customer_id=customer.customer_id,

            router_id=router.router_id,

            router_account_id=router_account.router_account_id,

            subscription_id=subscription.subscription_id,

            plan_id=plan.plan_id,

            device_id=(

                device.device_id

                if device

                else None

            ),

            device_mac=device_mac,

            device_ip=device_ip,

            link_orig=link_orig,

            status=PendingLoginStatus.PENDING,

            expires_at=(

                datetime.now()

                +

                timedelta(
                    minutes=PendingLoginService.DEFAULT_EXPIRY_MINUTES,
                )

            ),

        )

        db.add(
            pending_login,
        )

        db.commit()

        db.refresh(
            pending_login,
        )

        return pending_login

    @staticmethod
    def get_by_token(
        db: Session,
        token: str,
    ) -> PendingLogin:

        return PendingLoginService._find_by_token(
            db,
            token,
        )

    @staticmethod
    def consume(
        db: Session,
        pending_login: PendingLogin,
    ) -> PendingLogin:

        PendingLoginService._validate_pending_login(
            pending_login,
        )

        pending_login.status = (
            PendingLoginStatus.CONSUMED
        )

        pending_login.consumed_at = (
            datetime.now()
        )

        db.commit()

        db.refresh(
            pending_login,
        )

        return pending_login

    @staticmethod
    def expire(
        db: Session,
        pending_login: PendingLogin,
    ) -> PendingLogin:

        pending_login.status = (
            PendingLoginStatus.EXPIRED
        )

        db.commit()

        db.refresh(
            pending_login,
        )

        return pending_login

    @staticmethod
    def delete_expired(
        db: Session,
    ) -> int:

        expired = (

            db.query(
                PendingLogin,
            )

            .filter(
                PendingLogin.status
                == PendingLoginStatus.EXPIRED,
            )

            .all()

        )

        count = len(
            expired,
        )

        for pending_login in expired:

            db.delete(
                pending_login,
            )

        db.commit()

        return count