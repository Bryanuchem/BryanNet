from functools import lru_cache

from app.core.settings import (
    settings,
)

from app.router_portal.schemas import (
    PortalConfigurationSchema,
)


class PortalConfiguration:

    """
    Router Portal configuration
    provider.
    """

    @staticmethod
    def build() -> PortalConfigurationSchema:
        
        return  PortalConfigurationSchema(

            # ==========================================================
            # Company Branding
            # ==========================================================

            company_name="BryanNet",

            company_tagline=(
                "Fast • Reliable • Unlimited Internet"
            ),

            logo_url="/router_portal/static/img/logo.svg",

            favicon_url="/router_portal/static/img/favicon.ico",

            theme_color="#2563EB",

            # ==========================================================
            # Browser
            # ==========================================================

            browser_title=(
                "BryanNet | Connect to Internet"
            ),

            meta_description=(
                "Secure internet access through BryanNet."
            ),

            # ==========================================================
            # Login Page
            # ==========================================================

            login_title="Welcome Back",

            login_description=(
                "Sign in to continue browsing."
            ),

            login_button_text=(
                "Connect to Internet"
            ),

            remember_device_text=(
                "Remember this device"
            ),

            username_placeholder=(
                "Enter your username"
            ),

            password_placeholder=(
                "Enter your password"
            ),

            # ==========================================================
            # Success Page
            # ==========================================================

            success_title=(
                "Connected Successfully"
            ),

            success_message=(
                "Your internet connection is now active. "
                "You will be redirected shortly."
            ),

            # ==========================================================
            # Error Page
            # ==========================================================

            error_title=(
                "Connection Failed"
            ),

            error_message=(
                "Unable to authenticate your account. "
                "Please verify your credentials and try again."
            ),

            # ==========================================================
            # Support
            # ==========================================================

            support_title="Need Help?",

            support_phone=(
                "+2348012345678"
            ),

            support_email=(
                "support@bryannet.ng"
            ),

            support_whatsapp=(
                "https://wa.me/2348012345678"
            ),

            support_telegram=(
                "https://t.me/bryannet"
            ),

            # ==========================================================
            # Footer
            # ==========================================================

            footer_text=(
                "Powered by BryanNet."
            ),

            # ==========================================================
            # Redirect
            # ==========================================================

            default_redirect_url=(
                "https://www.google.com"
            ),

            redirect_delay=5,

            # ==========================================================
            # Feature Flags
            # ==========================================================

            remember_device_enabled=True,

            show_support_links=True,

            show_company_tagline=True,

            show_footer=True,

        )


@lru_cache
def get_portal_configuration(
) -> PortalConfigurationSchema:

    return PortalConfiguration.build()


portal_configuration = (
    get_portal_configuration()
)