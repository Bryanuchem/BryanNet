from fastapi import (
    Request,
)

from app.router_portal.service import (
    RouterPortalService,
)

from app.router_portal.schemas import (
    RouterHotspotContextSchema,
)


class RouterPortalContextBuilder:
    """
    Converts RouterOS request data into a
    RouterHotspotContextSchema.

    This class performs request parsing only.
    """

    @staticmethod
    def _as_bool(
        value,
    ):

        return (

            str(value)

            .strip()

            .lower()

            in (

                "true",

                "1",

                "yes",

                "on",

            )

        )

    # ==========================================================
    # Request Builder
    # ==========================================================

    @staticmethod
    def from_request(
        request: Request,
    ) -> RouterHotspotContextSchema:

        params = request.query_params

        hotspot = (

            RouterPortalService

            .build_hotspot_context(

                # ======================================================
                # RouterOS Login
                # ======================================================

                username=params.get(
                    "username",
                ),

                ip_address=params.get(
                    "ip",
                ),

                mac_address=params.get(
                    "mac",
                ),

                # ======================================================
                # Existing fields
                # ======================================================

                link_login=params.get(
                    "link-login",
                ),

                link_login_only=params.get(
                    "link-login-only",
                ),

                link_logout=params.get(
                    "link-logout",
                ),

                link_status=params.get(
                    "link-status",
                ),

                link_orig=params.get(
                    "link-orig",
                ),

                link_orig_esc=params.get(
                    "link-orig-esc",
                ),

                link_redirect=params.get(
                    "link-redirect",
                ),

                link_redirect_esc=params.get(
                    "link-redirect-esc",
                ),

                error_message=(

                    RouterPortalService

                    .translate_router_error(

                        params.get(
                            "error",
                        ),

                    )

                ),

                chap_id=params.get(
                    "chap-id",
                ),

                chap_challenge=params.get(
                    "chap-challenge",
                ),

                popup=(
                    RouterPortalContextBuilder._as_bool(
                        params.get(
                            "popup",
                        ),
                    )
                ),

                hostname=params.get(
                    "hostname",
                ),

                location_id=params.get(
                    "location-id",
                ),

                location_name=params.get(
                    "location-name",
                ),

                http_status=params.get(
                    "http-status",
                ),

                http_header=params.get(
                    "http-header",
                ),

            )

        )

        hotspot.login_token = params.get(
            "login_token",
        )

        return hotspot

    # ==========================================================
    # Form Builder
    # ==========================================================

    @staticmethod
    def from_form(
        form,
    ) -> RouterHotspotContextSchema:

        hotspot = (

            RouterPortalService

            .build_hotspot_context(

                link_login=form.get(
                    "link_login",
                ),

                link_login_only=form.get(
                    "link_login_only",
                ),

                link_logout=form.get(
                    "link_logout",
                ),

                link_status=form.get(
                    "link_status",
                ),

                link_orig=form.get(
                    "link_orig",
                ),

                link_orig_esc=form.get(
                    "link_orig_esc",
                ),

                link_redirect=form.get(
                    "link_redirect",
                ),

                link_redirect_esc=form.get(
                    "link_redirect_esc",
                ),

                chap_id=form.get(
                    "chap_id",
                ),

                chap_challenge=form.get(
                    "chap_challenge",
                ),

                popup=(

                    RouterPortalContextBuilder

                    ._as_bool(

                        form.get(
                            "popup",
                        )

                    )

                ),

                location_id=form.get(
                    "location_id",
                ),

                location_name=form.get(
                    "location_name",
                ),

                http_status=form.get(
                    "http_status",
                ),

                http_header=form.get(
                    "http_header",
                ),

            )

        )

        hotspot.username = form.get(
            "username",
        )

        hotspot.mac_address = form.get(
            "mac",
        )

        hotspot.ip_address = form.get(
            "ip",
        )

        hotspot.remember_device = (

            RouterPortalContextBuilder

            ._as_bool(

                form.get(
                    "remember_device",
                )

            )

        )

        return hotspot
    
    # ==========================================================
    # Preview Builder
    # ==========================================================

    @staticmethod
    def from_preview(
    ) -> RouterHotspotContextSchema:
        """
        Preview-only hotspot context.

        These values DO NOT originate from RouterOS.
        They exist solely so the portal can be rendered
        locally without an actual MikroTik hotspot.
        """

        hotspot = (

            RouterPortalService

            .build_hotspot_context(

                link_login="/portal/preview/login",

                link_login_only="/portal/preview/login",

                link_logout="/portal/preview/logout",

                link_status="/portal/preview/status",

                link_orig="https://google.com",

                link_orig_esc="https%3A%2F%2Fgoogle.com",

                link_redirect="https://google.com",

                link_redirect_esc="https%3A%2F%2Fgoogle.com",

                error_message="Invalid username or password.",

                chap_id="preview-chap-id",

                chap_challenge="preview-chap-challenge",

                popup=False,

            )

        )

        # ======================================================
        # Preview placeholders only.
        #
        # These values DO NOT exist in production.
        # RouterOS supplies the real values at runtime.
        # ======================================================

        hotspot.username = "08123456789"

        hotspot.ip_address = "192.168.88.25"

        hotspot.mac_address = "08:55:31:AB:4F:29"

        hotspot.session_duration = "2h 15m 44s"

        hotspot.upload_usage = "142 MB"

        hotspot.download_usage = "1.82 GB"

        # ======================================================
        # BryanNet preview placeholders.
        #
        # These values simulate information supplied by
        # BryanNet after successful authentication.
        # ======================================================

        hotspot.customer_name = "User XYZ"

        hotspot.plan_name = "Unlimited Premium"

        hotspot.plan_speed = "10 Mbps"

        hotspot.device_name = "Samsung Galaxy S24"

        # ======================================================
        # RouterOS compatibility placeholders.
        #
        # These values are used by compatibility templates
        # (redirect.html, rlogin.html, radvert.html).
        # RouterOS provides the real values at runtime.
        # ======================================================

        hotspot.hostname = "10.20.0.1"

        hotspot.location_id = "BryanNet"

        hotspot.location_name = "BryanNet Hotspot"

        hotspot.http_status = "302"

        hotspot.http_header = "Location"

        return hotspot