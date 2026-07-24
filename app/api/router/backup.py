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
        "Router Backup",
    ],

)


# ==========================================================
# Router Files
# ==========================================================

@router.get(

    "/{router_id}/files",

)

def list_router_files(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_router_files(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/files/{file_id}",

)

def get_router_file(
    router_id: int,
    file_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_router_file(

            db,

            router_id,

            file_id,

        )

    )


# ==========================================================
# Backup Schedules
# ==========================================================

@router.get(

    "/{router_id}/backup/schedules",

)

def list_backup_schedules(
    router_id: int,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.list_backup_schedules(

            db,

            router_id,

        )

    )


@router.get(

    "/{router_id}/backup/schedules/{schedule_id}",

)

def get_backup_schedule(
    router_id: int,
    schedule_id: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.get_backup_schedule(

            db,

            router_id,

            schedule_id,

        )

    )


# ==========================================================
# Commands
# ==========================================================

@router.post(

    "/{router_id}/backup/create",

)

def create_backup(
    router_id: int,
    name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.create_backup(

            db,

            router_id,

            name,

        )

    )


@router.post(

    "/{router_id}/backup/export",

)

def create_export(
    router_id: int,
    name: str,
    db: Session = Depends(
        get_db,
    ),
    _=Depends(
        get_current_admin,
    ),
):

    return (

        RouterService.create_export(

            db,

            router_id,

            name,

        )

    )