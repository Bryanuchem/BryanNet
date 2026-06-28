from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.plan import (
    PlanCreate,
    PlanResponse,
)

from app.services.plan_service import PlanService

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.get(
    "/",
    response_model=list[PlanResponse],
)
def get_plans(
    db: Session = Depends(get_db),
):
    return PlanService.get_all_plans(db)


@router.post(
    "/",
    response_model=PlanResponse,
    status_code=201,
)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db),
):
    return PlanService.create_plan(db, plan)


@router.put(
    "/{plan_id}",
    response_model=PlanResponse,
)
def update_plan(
    plan_id: int,
    plan: PlanCreate,
    db: Session = Depends(get_db),
):
    return PlanService.update_plan(
        db=db,
        plan_id=plan_id,
        plan=plan,
    )


@router.patch(
    "/{plan_id}/status",
    response_model=PlanResponse,
)
def update_plan_status(
    plan_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
):
    return PlanService.set_plan_status(
        db=db,
        plan_id=plan_id,
        is_active=is_active,
    )
    
@router.delete(
    "/{plan_id}",
    status_code=200,
)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
):
    return PlanService.delete_plan(
        db=db,
        plan_id=plan_id,
    )    