from fastapi import FastAPI

from app.api.customer import router as customer_router
from app.api.plan import router as plan_router
from app.api.subscription import router as subscription_router
from app.api.device import router as device_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api import session

app = FastAPI(
    title="BryanNet API"
)

app.include_router(
    customer_router,
    prefix="/api/v1"
)

app.include_router(
    plan_router,
    prefix="/api/v1"
)

app.include_router(
    subscription_router,
    prefix="/api/v1"
)

app.include_router(
    device_router,
    prefix="/api/v1"
)

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    session.router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "message": "BryanNet API Running"
    }