from fastapi import (
    APIRouter,
    Depends,
)

from pydantic import (
    BaseModel,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.services.router_operations_service import (
    RouterOperationsService,
)

router = APIRouter(

    prefix="/router-operations",

    tags=[
        "Router Operations",
    ],

)


# ==========================================================
# Request Schemas
# ==========================================================

class CustomerMigrationRequest(
    BaseModel,
):

    target_router_id: int


class RouterMigrationRequest(
    BaseModel,
):

    target_router_id: int


# ==========================================================
# Repair
# ==========================================================

@router.post(

    "/repair",

)

def repair_assignments(

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterOperationsService

        .repair_assignments(

            db,

        )

    )


# ==========================================================
# Rebalance
# ==========================================================

@router.post(

    "/rebalance",

)

def rebalance(

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterOperationsService

        .rebalance(

            db,

        )

    )


# ==========================================================
# Customer Migration
# ==========================================================

@router.post(

    "/customers/{customer_id}/migrate",

)

def migrate_customer(

    customer_id: int,

    request: CustomerMigrationRequest,

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterOperationsService

        .migrate_customer(

            db,

            customer_id,

            request.target_router_id,

        )

    )


# ==========================================================
# Router Migration
# ==========================================================

@router.post(

    "/routers/{router_id}/migrate",

)

def migrate_router(

    router_id: int,

    request: RouterMigrationRequest,

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterOperationsService

        .migrate_router(

            db,

            router_id,

            request.target_router_id,

        )

    )