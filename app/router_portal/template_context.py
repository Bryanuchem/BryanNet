from app.router_portal.config import (
    portal_configuration,
)

from app.router_portal.schemas import (
    RouterHotspotContextSchema,
)


class PortalTemplateContext:

    @staticmethod
    def build(
        hotspot: RouterHotspotContextSchema,
        request=None,
        static_url: str = "",
        build_mode: bool = False,
        **kwargs,
    ) -> dict:

        context = {

            "request": request,

            "settings": portal_configuration,

            "hotspot": hotspot,

            "static_url": static_url,

            "logo_url": f"{static_url}/img/logo.svg",

            "favicon_url": f"{static_url}/img/favicon.ico",

        }

        context.update(kwargs)

        if build_mode:

            # ==================================================
            # RouterOS placeholders
            # These are converted into $(...) variables in the
            # generated hotspot package.
            # ==================================================

            hotspot.link_login = "$(link-login)"

            hotspot.link_login_only = "$(link-login-only)"

            hotspot.link_logout = "$(link-logout)"

            hotspot.link_status = "$(link-status)"

            hotspot.link_orig = "$(link-orig)"

            hotspot.link_orig_esc = "$(link-orig-esc)"

            hotspot.link_redirect = "$(link-redirect)"

            hotspot.link_redirect_esc = "$(link-redirect-esc)"

            hotspot.chap_id = "$(chap-id)"

            hotspot.chap_challenge = "$(chap-challenge)"

            hotspot.username = "$(username)"

            hotspot.ip_address = "$(ip)"

            hotspot.mac_address = "$(mac)"

            hotspot.session_duration = "$(uptime)"

            hotspot.upload_usage = "$(bytes-out-nice)"

            hotspot.download_usage = "$(bytes-in-nice)"

            # ==================================================
            # BryanNet Runtime Fields
            #
            # RouterOS cannot populate BryanNet-specific values
            # such as customer, plan or device information.
            #
            # Clear preview values so they are not baked into the
            # generated hotspot package. These fields will be
            # populated at runtime by the BryanNet portal.
            # ==================================================

            hotspot.customer_name = None

            hotspot.plan_name = None

            hotspot.plan_speed = None

            hotspot.device_name = None
            
        return context