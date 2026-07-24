from fastapi import Request

from fastapi.responses import HTMLResponse


from app.router_portal.schemas import (
    RouterHotspotContextSchema,
)

from app.router_portal.templates import (
    templates,
)

from app.router_portal.template_context import (
    PortalTemplateContext,
)

class PortalRenderer:

    """
    Responsible for rendering
    captive portal templates.
    """

    # ==========================================================
    # Login
    # ==========================================================

    @classmethod
    def login(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="login.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

            )

        )

    # ==========================================================
    # RouterOS Login Handoff
    # ==========================================================

    @classmethod
    def router_login(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
        username: str,
        password: str,
        login_token: str | None = None,
        connected_url: str | None = None,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="router_login.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

                username=username,

                password=password,

                login_token=login_token,
                
                connected_url=connected_url,

            ),

        )

    # ==========================================================
    # Status
    # ==========================================================

    @classmethod
    def status(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="status.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

            ),

        )

    # ==========================================================
    # Connected
    # ==========================================================

    @classmethod
    def connected(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="alogin.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(

                    request.url_for(

                        "router_portal.static",

                        path="",

                    )

                ).rstrip("/"),

            ),

        )

    # ==========================================================
    # Success
    # ==========================================================

    @classmethod
    def success(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="success.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

            )

        )

    # ==========================================================
    # Error
    # ==========================================================

    @classmethod
    def error(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

            )

        )
    
# ==========================================================
# Logout
# ==========================================================

    @classmethod
    def logout(
        cls,
        request: Request,
        hotspot: RouterHotspotContextSchema,
    ) -> HTMLResponse:

        return templates.TemplateResponse(

            request=request,

            name="logout.html",

            context=PortalTemplateContext.build(

                request=request,

                hotspot=hotspot,

                static_url=str(
                    request.url_for(
                        "router_portal.static",
                        path="",
                    )
                ).rstrip("/"),

            ),

        )