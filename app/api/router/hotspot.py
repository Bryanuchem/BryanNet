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
        "Router Hotspot",
    ],

)


# ==========================================================
# Hotspot Profiles
# ==========================================================

@router.get(

    "/{router_id}/hotspot/profiles",

)

def list_hotspot_profiles(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_hotspot_profiles(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/hotspot/profiles/{profile_id}",

)

def get_hotspot_profile(
    router_id: int,
    profile_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_hotspot_profile(

            db,

            router_id,

            profile_id,

        )

    )


# ==========================================================
# Hotspot Servers
# ==========================================================

@router.get(

    "/{router_id}/hotspot/servers",

)

def list_hotspot_servers(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_hotspot_servers(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/hotspot/servers/{server_id}",

)

def get_hotspot_server(
    router_id: int,
    server_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_hotspot_server(

            db,

            router_id,

            server_id,

        )

    )


# ==========================================================
# Hotspot Users
# ==========================================================

@router.get(

    "/{router_id}/hotspot/users",

)

def list_hotspot_users(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_hotspot_users(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/hotspot/users/{user_id}",

)

def get_hotspot_user(
    router_id: int,
    user_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_hotspot_user(

            db,

            router_id,

            user_id,

        )

    )


# ==========================================================
# Active Sessions
# ==========================================================

@router.get(

    "/{router_id}/hotspot/active",

)

def list_hotspot_active(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_hotspot_active(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/hotspot/active/{session_id}",

)

def get_hotspot_active_session(
    router_id: int,
    session_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_hotspot_active_session(

            db,

            router_id,

            session_id,

        )

    )