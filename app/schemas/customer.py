from pydantic import BaseModel

from app.schemas.types import (
    FullName,
    PhoneNumber,
    PositiveInt,
)


class CustomerCreate(BaseModel):

    phone_number: PhoneNumber

    full_name: FullName


class CustomerUpdate(BaseModel):

    phone_number: PhoneNumber

    full_name: FullName


class CustomerOnboardingStart(BaseModel):

    telegram_user_id: PositiveInt


class CustomerUpdateName(BaseModel):

    telegram_user_id: PositiveInt

    full_name: FullName


class CustomerUpdatePhone(BaseModel):

    telegram_user_id: PositiveInt

    phone_number: PhoneNumber


class CustomerResponse(BaseModel):

    customer_id: int

    phone_number: str | None = None

    full_name: str | None = None

    telegram_user_id: int | None = None

    is_registered: bool
    
    status: str

    registration_step: str

    class Config:

        from_attributes = True
        
class CustomerListItem(BaseModel):

    customer_id: int

    phone_number: str | None = None

    full_name: str | None = None

    telegram_user_id: int | None = None

    is_registered: bool
    
    status: str

    registration_step: str

    class Config:

        from_attributes = True        