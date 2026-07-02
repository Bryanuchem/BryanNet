from datetime import UTC
from datetime import datetime

from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


# ==========================================================
# Health
# ==========================================================

@router.get("/")
def health_check():

    return {

        "status": "healthy",

        "service": "BryanNet API",

        "timestamp": datetime.now(
            UTC,
        ).isoformat(),

    }