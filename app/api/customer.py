from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerOnboardingStart,
    CustomerUpdateName,
    CustomerUpdatePhone,
    CustomerResponse,
)

from app.services.customer_service import (
    CustomerService
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/register",
    response_model=CustomerResponse
)
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    return CustomerService.register_customer(
        db=db,
        phone_number=customer.phone_number,
        full_name=customer.full_name,
        telegram_user_id=customer.telegram_user_id
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):

    return CustomerService.update_customer(
        db=db,
        customer_id=customer_id,
        customer_data=customer,
    )


@router.post(
    "/onboarding/start",
    response_model=CustomerResponse
)
def start_onboarding(
    customer: CustomerOnboardingStart,
    db: Session = Depends(get_db)
):

    return CustomerService.start_onboarding(
        db=db,
        telegram_user_id=customer.telegram_user_id
    )


@router.patch(
    "/onboarding/name",
    response_model=CustomerResponse
)
def update_name(
    customer: CustomerUpdateName,
    db: Session = Depends(get_db)
):

    result = CustomerService.update_name(
        db=db,
        telegram_user_id=customer.telegram_user_id,
        full_name=customer.full_name
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return result


@router.patch(
    "/onboarding/phone",
    response_model=CustomerResponse
)
def update_phone(
    customer: CustomerUpdatePhone,
    db: Session = Depends(get_db)
):

    result = CustomerService.update_phone(
        db=db,
        telegram_user_id=customer.telegram_user_id,
        phone_number=customer.phone_number
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return result


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_all_customers(
    db: Session = Depends(get_db)
):
    return CustomerService.get_all_customers(db)


@router.get(
    "/{phone_number}",
    response_model=CustomerResponse
)
def get_customer(
    phone_number: str,
    db: Session = Depends(get_db)
):

    return CustomerService.get_customer_by_phone(
        db=db,
        phone_number=phone_number
    )


@router.get(
    "/telegram/{telegram_user_id}",
    response_model=CustomerResponse
)
def get_customer_by_telegram_id(
    telegram_user_id: int,
    db: Session = Depends(get_db)
):

    customer = CustomerService.get_customer_by_telegram_id(
        db=db,
        telegram_user_id=telegram_user_id
    )

    if customer is None:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer