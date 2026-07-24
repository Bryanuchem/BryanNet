from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.models.customer import (
    Customer,
)

from app.models.device import (
    Device,
)

from app.models.plan import (
    Plan,
)

from app.models.router_account import (
    RouterAccount,
)

from app.models.router_session import (
    RouterSession,
)

from app.models.subscription import (
    Subscription,
)

from app.enums import (
    PortalAuthenticationError,
)

from app.core.settings import settings  

class PortalAuthenticationResultSchema:

    def __init__(

        self,

        success: bool,

        customer: Customer | None = None,

        subscription: Subscription | None = None,

        plan: Plan | None = None,

        router_account: RouterAccount | None = None,

        device: Device | None = None,

        error: PortalAuthenticationError | None = None,

    ):

        self.success = success

        self.customer = customer

        self.subscription = subscription

        self.plan = plan

        self.router_account = router_account

        self.device = device

        self.error = error

class PortalLoginResultSchema:

    """
    Result returned by the
    portal login orchestration.

    This represents the complete
    login workflow, not just
    authentication.
    """

    def __init__(

        self,

        success: bool,

        authentication: (
            PortalAuthenticationResultSchema
            | None
        ) = None,

        device: Device | None = None,

        router_session: (
            RouterSession
            | None
        ) = None,

        portal_session=None,

        redirect_url: str | None = None,

        username: str | None = None,

        password: str | None = None,

        login_token: str | None = None,

        error: (
            PortalAuthenticationError
            | None
        ) = None,

    ):

        self.success = success

        self.authentication = authentication

        self.device = device

        self.router_session = router_session

        self.portal_session = portal_session

        self.redirect_url = redirect_url

        #
        # RouterOS handoff credentials.
        #
        # These credentials are carried only for the
        # lifetime of the current request so the
        # controller can render the RouterOS handoff
        # page. They are never persisted.
        #

        self.username = username

        self.password = password

        #
        # Pending login token carried through the
        # RouterOS login handoff.
        #

        self.login_token = login_token

        self.error = error

class LoginRequestSchema(
    BaseModel,
):
    """
    Login credentials submitted
    from the captive portal.
    """

    username: str = Field(
        min_length=1,
        max_length=128,
    )

    password: str = Field(
        min_length=1,
        max_length=128,
    )

    mac_address: str | None = None 

    link_orig: str | None = None

    ip_address: str | None = None

    remember_device: bool = (
        False
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

class RouterCallbackSchema(
    BaseModel,
):
    """
    RouterOS callback payload.

    This schema represents the information returned
    by RouterOS after a successful hotspot login or
    logout. It provides the normalized payload used
    by SessionTrackingService.
    """

    # ======================================================
    # Router Identity
    # ======================================================

    username: str = Field(
        min_length=1,
        max_length=128,
    )

    router_session_id: str | None = None

    ip_address: str | None = None

    mac_address: str | None = None

    login_by: str | None = None

    # ======================================================
    # Session Statistics
    # ======================================================

    bytes_in: int = 0

    bytes_out: int = 0

    packets_in: int = 0

    packets_out: int = 0

    # ======================================================
    # Disconnect
    # ======================================================

    disconnect_reason: str | None = None

    # ======================================================
    # Model Configuration
    # ======================================================

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

class RouterPortalContextSchema(
    BaseModel,
):
    """
    Context supplied
    to Jinja templates.
    """

    page_title: str

    page_description: str

    settings: PortalConfigurationSchema

class RouterHotspotContextSchema(
    BaseModel,
):
    """
    RouterOS hotspot context.

    Field names intentionally match the
    official RouterOS hotspot placeholders.

    This allows BryanNet to preserve the
    RouterOS authentication protocol
    without translation.
    """

    # ======================================================
    # RouterOS Login
    # ======================================================

    link_login: str | None = None

    link_login_only: str | None = None

    link_logout: str | None = None

    link_status: str | None = None

    # ======================================================
    # RouterOS Redirects
    # ======================================================

    link_orig: str | None = None

    link_orig_esc: str | None = None

    link_redirect: str | None = None

    link_redirect_esc: str | None = None

    # ======================================================
    # RouterOS Session
    # ======================================================

    username: str | None = None

    ip_address: str | None = None

    mac_address: str | None = None

    popup: bool = False

    # ======================================================
    # BryanNet Session
    # ======================================================

    #
    # These fields are populated by BryanNet and are
    # independent of RouterOS. They provide the customer
    # connection summary displayed after successful login.
    #

    customer_name: str | None = None

    plan_name: str | None = None

    plan_speed: str | None = None

    device_name: str | None = None

    #
    # Pending login token generated by BryanNet.
    #
    # This token is carried during the RouterOS
    # hotspot login flow so BryanNet can associate
    # the RouterOS callback with the previously
    # authenticated customer.
    #

    login_token: str | None = None
    
    # ======================================================
    # RouterOS CHAP
    # ======================================================

    chap_id: str | None = None

    chap_challenge: str | None = None

    # ======================================================
    # Portal
    # ======================================================

    remember_device: bool = False

    error_message: str | None = None

    session_duration: str | None = None

    upload_usage: str | None = None

    download_usage: str | None = None

    # ======================================================
    # RouterOS Compatibility
    # ======================================================

    #
    # These fields are required by RouterOS compatibility
    # pages (redirect, rlogin, radvert, xml, api.json).
    #
    # They are supplied by RouterOS when available and
    # otherwise populated with preview defaults.
    #

    hostname: str | None = None

    location_id: str | None = None

    location_name: str | None = None

    http_status: str | None = None

    http_header: str | None = None
    

class LoginResultSchema(
    BaseModel,
):
    """
    Result returned after
    attempting authentication.
    """

    success: bool

    message: str

    redirect_url: Optional[
        str
    ] = None


class ErrorPageSchema(
    BaseModel,
):
    """
    Error page context.
    """

    title: str

    message: str

    retry_url: Optional[
        str
    ] = None


class SuccessPageSchema(
    BaseModel,
):
    """
    Success page context.
    """

    title: str

    message: str

    redirect_url: Optional[
        str
    ] = None

    redirect_delay: int = 3
    
class PortalConfigurationSchema(BaseModel):

    # ======================================================
    # Branding
    # ======================================================

    company_name: str

    company_tagline: str

    logo_url: str

    favicon_url: str

    theme_color: str = "#2563EB"

    # ======================================================
    # Browser
    # ======================================================

    browser_title: str

    meta_description: str

    # ==========================================================
    # Backend
    # ==========================================================

    portal_login_url: str = (
        settings.portal_login_url
    )

    portal_logout_url: str = (
        settings.portal_logout_url
    )

    # ======================================================
    # Login
    # ======================================================

    login_title: str

    login_description: str

    login_button_text: str

    remember_device_text: str = (
        "Remember this device"
    )

    username_placeholder: str = (
        "Enter your username"
    )

    password_placeholder: str = (
        "Enter your password"
    )

    # ======================================================
    # Support
    # ======================================================

    support_title: str = (
        "Need Help?"
    )

    support_phone: Optional[str] = None

    support_email: Optional[str] = None

    support_whatsapp: Optional[str] = None

    support_telegram: Optional[str] = None

    # ======================================================
    # Success
    # ======================================================

    success_title: str

    success_message: str

    # ======================================================
    # Error
    # ======================================================

    error_title: str

    error_message: str

    # ======================================================
    # Footer
    # ======================================================

    footer_text: str

    # ======================================================
    # Navigation
    # ======================================================

    default_redirect_url: str = "/"

    redirect_delay: int = 3

    # ======================================================
    # Feature Flags
    # ======================================================

    remember_device_enabled: bool = (
        True
    )

    show_support_links: bool = (
        True
    )

    show_company_tagline: bool = (
        True
    )

    show_footer: bool = (
        True
    )