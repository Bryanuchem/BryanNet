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

from app.services.router_account_service import (
    RouterAccountService,
)

router = APIRouter(

    prefix="/router-accounts",

    tags=[
        "Router Account Runtime",
    ],

)


# ==========================================================
# Synchronization
# ==========================================================

@router.post(

    "/{router_account_id}/synchronize",

)

def synchronize_router_account(
    router_account_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    account = (

        RouterAccountService

        .get_account(

            db,

            router_account_id,

        )

    )

    return (

        RouterAccountService

        .synchronize_customer_access(

            db,

            account.customer_id,

        )

    )


# ==========================================================
# Disconnect
# ==========================================================

@router.post(

    "/{router_account_id}/disconnect",

)

def disconnect_router_account(
    router_account_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    account = (

        RouterAccountService

        .get_account(

            db,

            router_account_id,

        )

    )

    context = (

        RouterAccountService

        .build_router_context(

            db,

            account.customer_id,

        )

    )

    return (

        RouterAccountService

        .disconnect_customer(

            db,

            context,

        )

    )


# ==========================================================
# Enable
# ==========================================================

@router.post(

    "/{router_account_id}/enable",

)

def enable_router_account(
    router_account_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    account = (

        RouterAccountService

        .activate_account(

            db,

            router_account_id,

        )

    )

    RouterAccountService.synchronize_customer_access(

        db,

        account.customer_id,

    )

    return {

        "success": True,

        "message":

            "Router account enabled.",

    }


# ==========================================================
# Disable
# ==========================================================

@router.post(

    "/{router_account_id}/disable",

)

def disable_router_account(
    router_account_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    account = (

        RouterAccountService

        .suspend_account(

            db,

            router_account_id,

        )

    )

    RouterAccountService.synchronize_customer_access(

        db,

        account.customer_id,

    )

    return {

        "success": True,

        "message":

            "Router account disabled.",

    }