from pydantic import BaseModel


class CustomerCreate(BaseModel):
    phone_number: str
    full_name: str
    telegram_user_id: int | None = None


class CustomerUpdate(BaseModel):
    phone_number: str
    full_name: str


class CustomerOnboardingStart(BaseModel):
    telegram_user_id: int


class CustomerUpdateName(BaseModel):
    telegram_user_id: int
    full_name: str


class CustomerUpdatePhone(BaseModel):
    telegram_user_id: int
    phone_number: str


class CustomerResponse(BaseModel):
    customer_id: int
    phone_number: str | None = None
    full_name: str | None = None
    telegram_user_id: int | None = None
    is_registered: bool
    registration_step: str

    class Config:
        from_attributes = True