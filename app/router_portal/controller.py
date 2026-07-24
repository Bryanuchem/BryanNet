from fastapi import (
    APIRouter,
    Request,
    Depends,
)

from app.core.settings import (
    settings,
)

from fastapi.responses import (
    HTMLResponse,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.router_portal.context_builder import (
    RouterPortalContextBuilder,
)

from app.router_portal.portal_authentication_message_service import (
    PortalAuthenticationMessageService,
)

from app.router_portal.portal_login_service import (
    PortalLoginService,
)

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.router_portal.renderer import (
    PortalRenderer,
)

from app.router_portal.schemas import (
    LoginRequestSchema,
)

from app.services.session_lifecycle_service import (
    SessionLifecycleService,
)

router = APIRouter(
    prefix="/portal",
    tags=["Router Portal"],
)


# ==========================================================
# Login Page
# ==========================================================

@router.get(
    "/login",
    response_class=HTMLResponse,
)
async def login_page(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_request(

            request,

        )

    )

    return (

        PortalRenderer

        .login(

            request=request,

            hotspot=hotspot,

        )

    )

# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_class=HTMLResponse,
)
async def login(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
) -> HTMLResponse:

    form = await request.form()

    # ==========================================================
    # Hotspot Context
    # ==========================================================

    hotspot = (

    RouterPortalContextBuilder

    .from_form(

        form,

    )

)
    
    # ==========================================================
    # Login Form
    # ==========================================================

    username = form.get(
        "username",
    )

    password = form.get(
        "password",
    )

    mac_address = form.get(
        "mac",
    )

    login_request = (

        LoginRequestSchema(

            username=(

                username.strip()

                if isinstance(
                    username,
                    str,
                )

                else ""

            ),

            password=(

                password

                if isinstance(
                    password,
                    str,
                )

                else ""

            ),

            mac_address=(

                mac_address

                if isinstance(
                    mac_address,
                    str,
                )

                else None

            ),

            ip_address=hotspot.ip_address,

            link_orig=hotspot.link_orig,

            remember_device=(

                form.get(
                    "remember_device",
                )

                == "on"

            ),

        )

    )

    # ==========================================================
    # Portal Login
    # ==========================================================

    result = (

        PortalLoginService

        .login(

            db=db,

            request=login_request,

        )

    )
    
    # ==========================================================
    # Login Failure
    # ==========================================================

    if not result.success:

        error = result.authentication

        hotspot.error_message = (

            PortalAuthenticationMessageService

            .get_message(

                error.error if error else None,

            )

        )

        hotspot.username = login_request.username

        hotspot.remember_device = login_request.remember_device

        return (

            PortalRenderer.login(

                request=request,

                hotspot=hotspot,

            )

        )

    # ==========================================================
    # BryanNet Session Summary
    #
    # Populate the hotspot context with authenticated
    # customer information for the captive portal pages.
    # ==========================================================

    authentication = result.authentication

    if authentication:

        customer = authentication.customer

        plan = authentication.plan

        device = result.device

        hotspot.customer_name = (

            str(customer.full_name)

            if customer

            else None

        )

        hotspot.plan_name = (

            str(plan.plan_name)

            if plan

            else None

        )

        hotspot.plan_speed = (

            f"{plan.speed_limit_mbps} Mbps"

            if plan

            else None

        )

        device = result.device

        hotspot.device_name = (

            str(device.device_name)

            if device

            else None

)
        
    hotspot.username = result.username

    # ==========================================================
    # RouterOS Login Handoff
    # ==========================================================

    router_username = (

        RouterUsernameService

        .to_router(

            result.username or "",

        )

    )

    # ==========================================================
    # RouterOS Success Callback
    # ==========================================================

    connected_url = (
        f"{settings.portal_base_url}"
        f"/api/v1/portal/connected"
        f"?login={result.login_token}"
    )

    return (

        PortalRenderer

        .router_login(

            request=request,

            hotspot=hotspot,

            username=router_username,

            password=result.password or "",

            login_token=result.login_token,
            
            connected_url=connected_url,

        )

    )


# ==========================================================
# Success Page
# ==========================================================

@router.get(
    "/success",
    response_class=HTMLResponse,
)
async def success_page(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_request(

            request,

        )

    )

    return (

        PortalRenderer

        .success(

            request=request,

            hotspot=hotspot,

        )

    )

# ==========================================================
# Connected Page (RouterOS Login Callback)
# ==========================================================

@router.get(
    "/connected",
    response_class=HTMLResponse,
)
async def connected_page(
    request: Request,
    db: Session = Depends(
        get_db,
    ),
) -> HTMLResponse:
    
    # ==========================================================
    # RouterOS Context
    # ==========================================================

    hotspot = (

        RouterPortalContextBuilder

        .from_request(

            request,

        )

    )

    # ==========================================================
    # Pending Login Token
    # ==========================================================

    login_token = request.query_params.get(
        "login",
    )

    lifecycle = (

        SessionLifecycleService

        .start_from_pending_login(

            db,

            login_token,

        )

    )

    pending_login = (

        lifecycle.pending_login

    )

    router_session = (

        lifecycle.router_session

    )

    portal_session = (

        lifecycle.portal_session

    )

    device = (

        lifecycle.device

    )

    customer = portal_session.customer

    router = portal_session.router

    router_account = portal_session.router_account

    #
    # Device supplied by the lifecycle service.
    #

    plan = pending_login.plan

    hotspot.username = router_account.username

    hotspot.customer_name = str(customer.full_name)

    hotspot.plan_name = str(plan.plan_name)

    hotspot.plan_speed = f"{plan.speed_limit_mbps} Mbps"
    
    hotspot.device_name = (

        str(device.device_name)

        if device

        else None

    )

    hotspot.ip_address = router_session.ip_address

    hotspot.mac_address = router_session.mac_address

    hotspot.link_orig = pending_login.link_orig

    hotspot.link_redirect = (

        pending_login.link_orig

        or hotspot.link_redirect

    )

    return (

        PortalRenderer.connected(

            request=request,

            hotspot=hotspot,

        )

    )

# ==========================================================
# Logout Page
# ==========================================================

@router.get(
    "/logout",
    response_class=HTMLResponse,
)
async def logout_page(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_request(

            request,

        )

    )

    return (

        PortalRenderer

        .logout(

            request=request,

            hotspot=hotspot,

        )

    )

# ==========================================================
# Error Page
# ==========================================================

@router.get(
    "/error",
    response_class=HTMLResponse,
)
async def error_page(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_request(

            request,

        )

    )

    return (

        PortalRenderer

        .error(

            request=request,

            hotspot=hotspot,

        )

    )