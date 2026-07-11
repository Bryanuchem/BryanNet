from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.constants.permissions import (
    Permissions,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.plan import (
    PlanCreate,
    PlanResponse,
)

from app.services.plan_service import (
    PlanService,
)

from app.schemas.page import (
    PageRequest,
)

from app.schemas.pagination import (
    PaginatedResponse,
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
    _=Depends(
        require_permission(
            Permissions.PLANS_CREATE,
        ),
    ),
):

    return (
        PlanService.create_plan(
            db=db,
            plan_data=plan,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.PLANS_EDIT,
        ),
    ),
):

    return (
        PlanService.update_plan_details(
            db=db,
            plan_id=plan_id,
            plan_data=plan,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.PLANS_ACTIVATE,
        ),
    ),
):

    return (
        PlanService.activate_plan(
            db=db,
            plan_id=plan_id,
            admin_id=admin.admin_user_id,
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
    _=Depends(
        require_permission(
            Permissions.PLANS_DEACTIVATE,
        ),
    ),
):

    return (
        PlanService.deactivate_plan(
            db=db,
            plan_id=plan_id,
            admin_id=admin.admin_user_id,
        )
    )


# ==========================================================
# Public Customer APIs
# ==========================================================    
@router.get(
    "/public",
    response_model=list[PlanResponse],
)
def get_public_plans(
    db: Session = Depends(get_db),
):

    return PlanService.get_active_plans(db)

# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=PaginatedResponse[
        PlanResponse,
    ],
)
def get_plans(

    search: str | None = None,

    is_active: bool | None = None,

    sort_by: str = "price",

    sort_order: str = "asc",

    page: PageRequest = Depends(),

    db: Session = Depends(
        get_db,
    ),

    admin=Depends(
        get_current_admin,
    ),

    _=Depends(
        require_permission(
            Permissions.PLANS_VIEW,
        ),
    ),

):

    return (
        PlanService.get_all_plans(

            db=db,

            page=page.page,

            page_size=page.page_size,

            search=search,

            is_active=is_active,

            sort_by=sort_by,

            sort_order=sort_order,

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
    _=Depends(
        require_permission(
            Permissions.PLANS_VIEW,
        ),
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
    _=Depends(
        require_permission(
            Permissions.PLANS_VIEW,
        ),
    ),
):

    return (
        PlanService.get_plan(
            db=db,
            plan_id=plan_id,
        )
    )