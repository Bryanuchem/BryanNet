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

from app.services.router_service import (
    RouterService
)

from app.services.router_provisioning_service import (
    RouterProvisioningService,
)

from app.services.router_context_service import (
    RouterContextService,
)

from app.services.router_session_service import (
    RouterSessionService,
)

from app.services.session_lifecycle_service import (
    SessionLifecycleService,
)

router = APIRouter(

    prefix="/router-accounts",

    tags=[
        "Router Account Runtime",
    ],

)

# ==========================================================
# Provisioning
# ==========================================================

@router.post(

    "/provision",

)

def provision_router_accounts(

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterAccountService

        .provision_active_accounts(

            db,

        )

    )

# ==========================================================
# Bulk Synchronization
# ==========================================================

@router.post(

    "/synchronize",

)

def synchronize_router_accounts(

    db: Session = Depends(

        get_db,

    ),

    _=Depends(

        get_current_admin,

    ),

):

    return (

        RouterProvisioningService

        .synchronize_active_accounts(

            db,

        )

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

        RouterProvisioningService

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

        RouterContextService

        .from_router_account(

            db,

            account.router_account_id,

        )

    )

    router_session = (

        RouterSessionService

        .get_active_session(

            db,

            router_account_id=(
                account.router_account_id
            ),

        )

    )

    if router_session:

        SessionLifecycleService.terminate_session(

            db,

            router_session=router_session,

            reason="admin_disconnect",

        )

    return (

        RouterService

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

    RouterProvisioningService.synchronize_customer_access(

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

    RouterProvisioningService.synchronize_customer_access(

        db,

        account.customer_id,

    )

    return {

        "success": True,

        "message":

            "Router account disabled.",

    }