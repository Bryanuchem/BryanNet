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

from app.services.router_service import (
    RouterService,
)

router = APIRouter(

    prefix="/routers",

    tags=[
        "Router Firewall",
    ],

)

# ==========================================================
# Filter Rules
# ==========================================================

@router.get(

    "/{router_id}/firewall/filter",

)

def list_filter_rules(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_filter_rules(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/firewall/filter/{rule_id}",

)

def get_filter_rule(
    router_id: int,
    rule_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_filter_rule(

            db,

            router_id,

            rule_id,

        )

    )


# ==========================================================
# NAT Rules
# ==========================================================

@router.get(

    "/{router_id}/firewall/nat",

)

def list_nat_rules(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_nat_rules(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/firewall/nat/{rule_id}",

)

def get_nat_rule(
    router_id: int,
    rule_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_nat_rule(

            db,

            router_id,

            rule_id,

        )

    )


# ==========================================================
# Mangle Rules
# ==========================================================

@router.get(

    "/{router_id}/firewall/mangle",

)

def list_mangle_rules(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_mangle_rules(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/firewall/mangle/{rule_id}",

)

def get_mangle_rule(
    router_id: int,
    rule_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_mangle_rule(

            db,

            router_id,

            rule_id,

        )

    )


# ==========================================================
# Raw Rules
# ==========================================================

@router.get(

    "/{router_id}/firewall/raw",

)

def list_raw_rules(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_raw_rules(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/firewall/raw/{rule_id}",

)

def get_raw_rule(
    router_id: int,
    rule_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_raw_rule(

            db,

            router_id,

            rule_id,

        )

    )