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
        "Router DHCP",
    ],

)


# ==========================================================
# DHCP Servers
# ==========================================================

@router.get(

    "/{router_id}/dhcp/servers",

)

def list_dhcp_servers(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_dhcp_servers(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/dhcp/servers/{server_id}",

)

def get_dhcp_server(
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

        RouterService.get_dhcp_server(

            db,

            router_id,

            server_id,

        )

    )


# ==========================================================
# DHCP Networks
# ==========================================================

@router.get(

    "/{router_id}/dhcp/networks",

)

def list_dhcp_networks(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_dhcp_networks(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/dhcp/networks/{network_id}",

)

def get_dhcp_network(
    router_id: int,
    network_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_dhcp_network(

            db,

            router_id,

            network_id,

        )

    )


# ==========================================================
# DHCP Options
# ==========================================================

@router.get(

    "/{router_id}/dhcp/options",

)

def list_dhcp_options(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_dhcp_options(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/dhcp/options/{option_id}",

)

def get_dhcp_option(
    router_id: int,
    option_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_dhcp_option(

            db,

            router_id,

            option_id,

        )

    )
    
# ==========================================================
# DHCP Leases
# ==========================================================

@router.get(
    "/routers/{router_id}/dhcp-leases",
)

def list_dhcp_leases(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (

        RouterService.list_dhcp_leases(

            db,

            router_id,

        )

    )


@router.get(
    "/routers/{router_id}/dhcp-leases/{lease_id}",
)

def get_dhcp_lease(
    router_id: int,
    lease_id: str,
    db: Session = Depends(
        get_db,
    ),
):

    return (

        RouterService.get_dhcp_lease(

            db,

            router_id,

            lease_id,

        )

    )