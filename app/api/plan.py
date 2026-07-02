from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.schemas.plan import (
    PlanCreate,
    PlanResponse,
)

from app.services.plan_service import (
    PlanService,
)


router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/",
    response_model=PlanResponse,
    status_code=201,
)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.create_plan(
            db=db,
            plan_data=plan,
        )
    )


@router.put(
    "/{plan_id}",
    response_model=PlanResponse,
)
def update_plan(
    plan_id: int,
    plan: PlanCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.update_plan_details(
            db=db,
            plan_id=plan_id,
            plan_data=plan,
        )
    )


@router.patch(
    "/{plan_id}/activate",
    response_model=PlanResponse,
)
def activate_plan(
    plan_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.activate_plan(
            db=db,
            plan_id=plan_id,
        )
    )


@router.patch(
    "/{plan_id}/deactivate",
    response_model=PlanResponse,
)
def deactivate_plan(
    plan_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.deactivate_plan(
            db=db,
            plan_id=plan_id,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[PlanResponse],
)
def get_all_plans(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.get_all_plans(
            db,
        )
    )


@router.get(
    "/active",
    response_model=list[PlanResponse],
)
def get_active_plans(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.get_active_plans(
            db,
        )
    )


@router.get(
    "/{plan_id}",
    response_model=PlanResponse,
)
def get_plan(
    plan_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        PlanService.get_plan(
            db=db,
            plan_id=plan_id,
        )
    )