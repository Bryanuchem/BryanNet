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

from app.schemas.customer import (
    CustomerCreate,
    CustomerOnboardingStart,
    CustomerResponse,
    CustomerUpdate,
    CustomerUpdateName,
    CustomerUpdatePhone,
)

from app.services.customer_service import (
    CustomerService,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


# ==========================================================
# Business Commands
# ==========================================================

@router.post(
    "/register",
    response_model=CustomerResponse,
)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.register_customer(
            db=db,
            phone_number=customer.phone_number,
            full_name=customer.full_name,
            telegram_user_id=customer.telegram_user_id,
        )
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.update_customer(
            db=db,
            customer_id=customer_id,
            customer_data=customer,
        )
    )


@router.patch(
    "/{customer_id}/activate",
    response_model=CustomerResponse,
)
def activate_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.activate_customer(
            db=db,
            customer_id=customer_id,
        )
    )


@router.patch(
    "/{customer_id}/deactivate",
    response_model=CustomerResponse,
)
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.deactivate_customer(
            db=db,
            customer_id=customer_id,
        )
    )


@router.post(
    "/onboarding/start",
    response_model=CustomerResponse,
)
def start_onboarding(
    customer: CustomerOnboardingStart,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        CustomerService.start_onboarding(
            db=db,
            telegram_user_id=customer.telegram_user_id,
        )
    )


@router.patch(
    "/onboarding/name",
    response_model=CustomerResponse,
)
def update_full_name(
    customer: CustomerUpdateName,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        CustomerService.update_full_name(
            db=db,
            telegram_user_id=customer.telegram_user_id,
            full_name=customer.full_name,
        )
    )


@router.patch(
    "/onboarding/phone",
    response_model=CustomerResponse,
)
def update_phone_number(
    customer: CustomerUpdatePhone,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        CustomerService.update_phone_number(
            db=db,
            telegram_user_id=customer.telegram_user_id,
            phone_number=customer.phone_number,
        )
    )


# ==========================================================
# Query Methods
# ==========================================================

@router.get(
    "/",
    response_model=list[CustomerResponse],
)
def get_all_customers(
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.get_all_customers(
            db,
        )
    )


@router.get(
    "/id/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.get_customer(
            db=db,
            customer_id=customer_id,
        )
    )


@router.get(
    "/phone/{phone_number}",
    response_model=CustomerResponse,
)
def get_customer_by_phone(
    phone_number: str,
    db: Session = Depends(
        get_db,
    ),
    admin=Depends(
        get_current_admin,
    ),
):

    return (
        CustomerService.get_customer_by_phone(
            db=db,
            phone_number=phone_number,
        )
    )


@router.get(
    "/telegram/{telegram_user_id}",
    response_model=CustomerResponse,
)
def get_customer_by_telegram_id(
    telegram_user_id: int,
    db: Session = Depends(
        get_db,
    ),
):

    return (
        CustomerService.get_customer_by_telegram_id(
            db=db,
            telegram_user_id=telegram_user_id,
        )
    )