from sqlalchemy.orm import (
    Session,
)

from app.models.router import (
    Router,
)

from app.models.router_account import (
    RouterAccount,
)


class RouterHotspotLoginService:

    """
    Orchestrates RouterOS hotspot login.

    Responsibilities

    - Resolve router
    - Resolve router account
    - Prepare RouterOS login
    - Delegate to the configured
      router provider (future)

    This service deliberately
    does NOT:

    - Authenticate customers
    - Validate subscriptions
    - Register devices
    - Render HTML
    """

    # ==========================================================
    # Public API
    # ==========================================================

    @staticmethod
    def login(
        db: Session,
        *,
        router: Router,
        router_account: RouterAccount,
        password: str,
        login_token: str,
    ):

        # ==========================================================
        # Validation
        # ==========================================================

        if not router:

            raise ValueError(

                "Router is required."

            )

        if not router_account:

            raise ValueError(

                "Router account is required."

            )

        if not password:

            raise ValueError(

                "Router password is required."

            )

        if not login_token:

            raise ValueError(

                "Login token is required."

            )
    
        # ==========================================================
        # Phase 5C
        #
        # RouterOS Hotspot login is
        # completed by the customer's
        # browser using the hidden
        # CHAP login form rendered by
        # router_login.html.
        #
        # Therefore there is nothing
        # to execute server-side here.
        #
        # Future router providers may
        # override this behaviour if
        # they support API-based
        # hotspot authentication.
        # ==========================================================

        return None

    @staticmethod
    def logout(
        db: Session,
        *,
        router: Router,
        router_account: RouterAccount,
    ):

        # ==========================================================
        # Validation
        # ==========================================================

        if not router:

            raise ValueError(

                "Router is required."

            )

        if not router_account:

            raise ValueError(

                "Router account is required."

            )

        # ==========================================================
        # Phase 5E
        #
        # RouterOS logout currently
        # occurs through the hotspot
        # logout endpoint.
        #
        # Future router providers may
        # perform API-based logout or
        # immediate session termination.
        # ==========================================================

        return None