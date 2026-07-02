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
):

    return (
        AdministrationService.get_overview(
            db,
        )
    )