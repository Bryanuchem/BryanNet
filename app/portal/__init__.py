from fastapi import APIRouter


from app.portal.session import (
    router as session_router,
)

from app.portal.onboarding import (
    router as onboarding_router,
)

from app.portal.plans import (
    router as plans_router,
)

from app.portal.devices import (
    router as devices_router,
)

from app.portal.subscriptions import (
    router as subscriptions_router,
)


from app.portal.payments import (
    router as payments_router,
)


router = APIRouter(
    prefix="/portal",
)


# ==========================================================
# Session
# ==========================================================

router.include_router(
    session_router,
)


# ==========================================================
# Onboarding
# ==========================================================

router.include_router(
    onboarding_router,
)


# ==========================================================
# Plans
# ==========================================================

router.include_router(
    plans_router,
)


# ==========================================================
# Devices
# ==========================================================

router.include_router(
    devices_router,
)


# ==========================================================
# Subscriptions
# ==========================================================

router.include_router(
    subscriptions_router,
)


# ==========================================================
# Payments
# ==========================================================

router.include_router(
    payments_router,
)
