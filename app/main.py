from fastapi import (
    FastAPI,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.api.administration import (
    router as administration_router,
)

from app.api.admin_session import (
    router as admin_session_router,
)

from app.api.auth import (
    router as auth_router,
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

from app.api.session import (
    router as session_router,
)

from app.api.subscription import (
    router as subscription_router,
)


app = FastAPI(

    title="BryanNet API",

    version="1.0.0",

    description="Backend API for the BryanNet ISP Management Platform",

)


# ==========================================================
# Middleware
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# ==========================================================
# API v1
# ==========================================================

API_PREFIX = "/api/v1"


app.include_router(
    auth_router,
    prefix=API_PREFIX,
)

app.include_router(
    administration_router,
    prefix=API_PREFIX,
)

app.include_router(
    admin_session_router,
    prefix=API_PREFIX,
)

app.include_router(
    dashboard_router,
    prefix=API_PREFIX,
)

app.include_router(
    customer_router,
    prefix=API_PREFIX,
)

app.include_router(
    plan_router,
    prefix=API_PREFIX,
)

app.include_router(
    subscription_router,
    prefix=API_PREFIX,
)

app.include_router(
    device_router,
    prefix=API_PREFIX,
)

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

app.include_router(
    health_router,
    prefix=API_PREFIX,
)


# ==========================================================
# Root
# ==========================================================

@app.get("/")
def root():

    return {

        "message": "BryanNet API Running",

        "version": "1.0.0",

    }