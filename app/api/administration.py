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

from app.constants.permissions import (
    Permissions,
)

from app.database.permission_dependencies import (
    require_permission,
)

from app.schemas.administration import (
    AdministrationOverviewResponse,
)

from app.services.administration_service import (
    AdministrationService,
)


router = APIRouter(
    prefix="/administration",
    tags=["Administration"],
)


# ==========================================================
# Administration
# ==========================================================

@router.get(
    "/overview",
    response_model=AdministrationOverviewResponse,
)
def get_administration_overview(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
    _=Depends(
        require_permission(
            Permissions.ADMINISTRATION_VIEW,
        ),
    ),
):

    return (
        AdministrationService.get_overview(
            db,
        )
    )