from fastapi import (
    APIRouter,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
)

from app.router_portal.context_builder import (
    RouterPortalContextBuilder,
)

from app.router_portal.renderer import (
    PortalRenderer,
)

router = APIRouter(
    prefix="/portal/preview",
    tags=["Router Portal Preview"],
)

# ==========================================================
# Login Preview
# ==========================================================

@router.get(
    "/login",
    response_class=HTMLResponse,
)
async def login_preview(
    request: Request,
) -> HTMLResponse:

    return (

        PortalRenderer.login(

            request=request,

            hotspot=(

                RouterPortalContextBuilder

                .from_preview()

            ),

        )

    )


# ==========================================================
# RouterOS Login Success Preview
# ==========================================================

@router.get(
    "/alogin",
    response_class=HTMLResponse,
)
async def alogin_preview(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_preview()

    )

    hotspot.error_message = None

    return (

        PortalRenderer.router_login(

            request=request,

            hotspot=hotspot,

            username="preview-user",

            password="preview-password",

        )

    )


# ==========================================================
# Status Preview
# ==========================================================

@router.get(
    "/status",
    response_class=HTMLResponse,
)
async def status_preview(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_preview()

    )

    hotspot.error_message = None

    return (

        PortalRenderer.status(

            request=request,

            hotspot=hotspot,

        )

    )


# ==========================================================
# Error Preview
# ==========================================================

@router.get(
    "/error",
    response_class=HTMLResponse,
)
async def error_preview(
    request: Request,
) -> HTMLResponse:

    return (

        PortalRenderer.error(

            request=request,

            hotspot=(

                RouterPortalContextBuilder

                .from_preview()

            ),

        )

    )


# ==========================================================
# Logout Preview
# ==========================================================

@router.get(
    "/logout",
    response_class=HTMLResponse,
)
async def logout_preview(
    request: Request,
) -> HTMLResponse:

    hotspot = (

        RouterPortalContextBuilder

        .from_preview()

    )

    hotspot.error_message = None

    return (

        PortalRenderer.logout(

            request=request,

            hotspot=hotspot,

        )

    )