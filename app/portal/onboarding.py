from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_db,
)

from app.schemas.portal_onboarding import (
    PortalOnboardingResponse,
    PortalOnboardingStart,
    PortalUpdateName,
    PortalUpdatePhone,
)

from app.services.portal.onboarding_service import (
    PortalOnboardingService,
)


router = APIRouter(
    prefix="/onboarding",
    tags=["Portal Onboarding"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/start",
    response_model=PortalOnboardingResponse,
)
def start_onboarding(
    request: PortalOnboardingStart,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalOnboardingService.start_onboarding(
            db,
            request,
        )
    )


@router.patch(
    "/name",
    response_model=PortalOnboardingResponse,
)
def update_full_name(
    request: PortalUpdateName,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalOnboardingService.update_full_name(
            db,
            request,
        )
    )


@router.patch(
    "/phone",
    response_model=PortalOnboardingResponse,
)
def update_phone_number(
    request: PortalUpdatePhone,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        PortalOnboardingService.update_phone_number(
            db,
            request,
        )
    )