from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.plan import (
    PlanResponse,
)

from app.services.plan_service import (
    PlanService,
)


router = APIRouter(
    prefix="/plans",
    tags=["Portal Plans"],
)


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[PlanResponse],
)
def get_available_plans(
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PlanService.get_active_plans(
            db,
        )
    )