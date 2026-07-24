from typing import cast

from sqlalchemy.orm import (
    Session,
)

from app.router_portal.portal_authentication_service import (
    PortalAuthenticationService,
)

from app.services.pending_login_service import (
    PendingLoginService,
)

from app.router_portal.router_hotspot_login_service import (
    RouterHotspotLoginService,
)

from app.models.router import (
    Router,
)

from app.models.router_account import (
    RouterAccount,
)

from app.router_portal.schemas import (
    LoginRequestSchema,
    PortalLoginResultSchema,
)

from app.services.device_registration_service import (
    DeviceRegistrationService,
)


class PortalLoginService:

    """
    Orchestrates the complete
    captive portal login flow.

    Responsibilities

    - Authenticate customer
    - Register / touch device
    - Prepare RouterOS login
    - Portal session creation (future)

    This service deliberately
    does NOT:

    - Render HTML
    - Return HTTP responses
    - Query templates
    """

    # ==========================================================
    # Public API
    # ==========================================================

    @staticmethod
    def login(
        db: Session,
        request: LoginRequestSchema,
    ) -> PortalLoginResultSchema:

        # ==========================================================
        # Authentication
        # ==========================================================

        authentication = (

            PortalAuthenticationService

            .authenticate(

                db=db,

                request=request,

            )

        )

        if not authentication.success:

            return (

                PortalLoginResultSchema(

                    success=False,

                    authentication=authentication,

                    error=authentication.error,

                )

            )

        router_account = cast(

            RouterAccount,

            authentication.router_account,

        )

        router = cast(

            Router,

            router_account.router,

        )

        # ==========================================================
        # Device Registration
        # ==========================================================

        device = authentication.device

        if (

            request.mac_address

            and

            authentication.customer

        ):

            device = (

                DeviceRegistrationService

                .register_or_touch(

                    db,

                    customer=authentication.customer,

                    mac_address=request.mac_address,

                )

            )

        pending_login = (

            PendingLoginService

            .create(

                db=db,

                customer=authentication.customer,

                router=router,

                router_account=router_account,

                subscription=authentication.subscription,

                plan=authentication.plan,

                device=device,

                device_mac=request.mac_address,

                device_ip=request.ip_address,

                link_orig=request.link_orig,

            )

        )

        # ==========================================================
        # RouterOS Login Preparation
        # ==========================================================

        RouterHotspotLoginService.login(

            db=db,

            router=router,

            router_account=router_account,

            password=request.password,

            login_token=pending_login.login_token,

        )


        # ==========================================================
        # Router Session
        #
        # Created after RouterOS
        # successfully completes
        # the browser login.
        # ==========================================================

        router_session = None

        # ==========================================================
        # Portal Session
        #
        # Created together with the
        # RouterSession after the
        # RouterOS login callback.
        # ==========================================================

        portal_session = None

        # ==========================================================
        # Success
        # ==========================================================

        return (

            PortalLoginResultSchema(

                success=True,

                authentication=authentication,

                device=device,

                router_session=router_session,

                portal_session=portal_session,

                username=cast(

                    str,

                    router_account.username,

                ),

                password=request.password,

                login_token=pending_login.login_token,

            )

        )