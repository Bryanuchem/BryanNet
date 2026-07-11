from typing import (
    Any,
    cast,
)

from fastapi import (
    FastAPI,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from slowapi import (
    _rate_limit_exceeded_handler,
)

from slowapi.errors import (
    RateLimitExceeded,
)

from slowapi.middleware import (
    SlowAPIMiddleware,
)

from app.api.administration import (
    router as administration_router,
)

from app.api.admin_session import (
    router as admin_session_router,
)

from app.api.admin_user import (
    router as admin_user_router,
)

from app.api.audit_log import (
    router as audit_log_router,
)

from app.api.auth import (
    router as auth_router,
)

from app.api.permission import (
    router as permission_router,
)

from app.api.automation import (
    router as automation_router,
)

from app.api.customer import (
    router as customer_router,
)

from app.api.dashboard import (
    router as dashboard_router,
)

from app.api.device import (
    router as device_router,
)

from app.api.health import (
    router as health_router,
)

from app.api.payment import (
    router as payment_router,
)

from app.api.plan import (
    router as plan_router,
)

from app.api.role import (
    router as role_router,
)

from app.api.session import (
    router as session_router,
)

from app.api.settings import (
    router as settings_router,
)

from app.api.subscription import (
    router as subscription_router,
)

from app.api.system_activity import (
    router as system_activity_router,
)

from app.core.exception_handlers import (
    register_exception_handlers,
)

from app.core.rate_limit import (
    limiter,
)

from app.core.request_logging import (
    RequestLoggingMiddleware,
)

from app.core.settings import (
    settings,
)


app = FastAPI(

    title=settings.app_name,

    version=settings.app_version,

    description="Backend API for the BryanNet ISP Management Platform",

)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    cast(
        Any,
        _rate_limit_exceeded_handler,
    ),
)


# ==========================================================
# Middleware
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        settings.frontend_origin,
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

app.add_middleware(
    SlowAPIMiddleware,
)

app.add_middleware(
    RequestLoggingMiddleware,
)


# ==========================================================
# API v1
# ==========================================================

API_PREFIX = settings.api_prefix


# ----------------------------------------------------------
# Authentication
# ----------------------------------------------------------

app.include_router(
    auth_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Dashboard
# ----------------------------------------------------------

app.include_router(
    dashboard_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Customers
# ----------------------------------------------------------

app.include_router(
    customer_router,
    prefix=API_PREFIX,
)

app.include_router(
    device_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Services
# ----------------------------------------------------------

app.include_router(
    plan_router,
    prefix=API_PREFIX,
)

app.include_router(
    subscription_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Operations
# ----------------------------------------------------------

app.include_router(
    payment_router,
    prefix=API_PREFIX,
)

app.include_router(
    automation_router,
    prefix=API_PREFIX,
)

app.include_router(
    session_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Administration
# ----------------------------------------------------------

app.include_router(
    administration_router,
    prefix=API_PREFIX,
)

app.include_router(
    admin_user_router,
    prefix=API_PREFIX,
)

app.include_router(
    role_router,
    prefix=API_PREFIX,
)

app.include_router(
    permission_router,
    prefix=API_PREFIX,
)

app.include_router(
    audit_log_router,
    prefix=API_PREFIX,
)

app.include_router(
    system_activity_router,
    prefix=API_PREFIX
)

app.include_router(
    admin_session_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Settings
# ----------------------------------------------------------

app.include_router(
    settings_router,
    prefix=API_PREFIX,
)


# ----------------------------------------------------------
# Health
# ----------------------------------------------------------

app.include_router(
    health_router,
    prefix=API_PREFIX,
)


# ==========================================================
# Exception Handlers
# ==========================================================

register_exception_handlers(
    app,
)


# ==========================================================
# Root
# ==========================================================

@app.get("/")
def root():

    return {

        "message": "BryanNet API Running",

        "version": settings.app_version,

    }