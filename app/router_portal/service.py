from app.router_portal.config import (
    portal_configuration,
)

from app.router_portal.schemas import (
    LoginRequestSchema,
    LoginResultSchema,
    RouterHotspotContextSchema,
)


class RouterPortalService:

    """
    Business logic for the
    Router Portal.
    """

    # ==========================================================
    # Hotspot Context
    # ==========================================================

    @staticmethod
    def build_hotspot_context(
        *,
        link_login: str | None = None,
        link_login_only: str | None = None,
        link_logout: str | None = None,
        link_status: str | None = None,
        link_orig: str | None = None,
        link_orig_esc: str | None = None,
        link_redirect: str | None = None,
        link_redirect_esc: str | None = None,
        error_message: str | None = None,
        chap_id: str | None = None,
        chap_challenge: str | None = None,
        popup: bool = False,
        # ==================================================
        # BryanNet Session
        # ==================================================
        customer_name: str | None = None,
        username: str | None = None,
        ip_address: str | None = None,
        mac_address: str | None = None,
        plan_name: str | None = None,
        plan_speed: str | None = None,
        device_name: str | None = None,
        hostname: str | None = None,
        location_id: str | None = None,
        location_name: str | None = None,
        http_status: str | None = None,
        http_header: str | None = None,
    ) -> RouterHotspotContextSchema:

        return RouterHotspotContextSchema(

            # ==================================================
            # RouterOS Login
            # ==================================================

            username=username,

            ip_address=ip_address,

            mac_address=mac_address,

            link_login=link_login,

            link_login_only=link_login_only,

            link_logout=link_logout,

            link_status=link_status,

            # ==================================================
            # RouterOS Redirects
            # ==================================================

            link_orig=link_orig,

            link_orig_esc=link_orig_esc,

            link_redirect=link_redirect,

            link_redirect_esc=link_redirect_esc,

            # ==================================================
            # RouterOS CHAP
            # ==================================================

            chap_id=chap_id,

            chap_challenge=chap_challenge,

            popup=popup,

            # ==================================================
            # BryanNet Session
            # ==================================================

            customer_name=customer_name,

            plan_name=plan_name,

            plan_speed=plan_speed,

            device_name=device_name,

            # ==================================================
            # Portal
            # ==================================================

            error_message=error_message,

            # ==================================================
            # RouterOS Compatibility
            # ==================================================

            hostname=hostname,

            location_id=location_id,

            location_name=location_name,

            http_status=http_status,

            http_header=http_header,

        )

    # ==========================================================
    # Login Validation
    # ==========================================================

    @staticmethod
    def validate_login(
        request: LoginRequestSchema,
    ) -> LoginResultSchema:

        if not request.username:

            return LoginResultSchema(

                success=False,

                message="Username is required.",

            )

        if not request.password:

            return LoginResultSchema(

                success=False,

                message="Password is required.",

            )

        return LoginResultSchema(

            success=True,

            message="Validation successful.",

            redirect_url=(
                portal_configuration
                .default_redirect_url
            ),

        )

    # ==========================================================
    # Error Translation
    # ==========================================================

    @staticmethod
    def translate_router_error(
        error: str | None,
    ) -> str | None:

        if not error:

            return None

        mapping = {

            "invalid username or password":
                "Incorrect username or password.",

            "user disabled":
                "Your account has been disabled.",

            "traffic limit reached":
                "Your data limit has been reached.",

            "session limit reached":
                "Maximum device limit reached.",

            "host limit reached":
                "Maximum device limit reached.",

        }

        return mapping.get(

            error.lower(),

            error,

        )

    # ==========================================================
    # Redirect
    # ==========================================================

    @staticmethod
    def get_redirect_url(
        hotspot: RouterHotspotContextSchema,
    ) -> str:

        if hotspot.link_redirect:

            return hotspot.link_redirect

        if hotspot.link_orig:

            return hotspot.link_orig

        return (
            portal_configuration
            .default_redirect_url
        )