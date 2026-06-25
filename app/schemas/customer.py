from pydantic import BaseModel


class CustomerCreate(BaseModel):
    phone_number: str
    full_name: str
    telegram_user_id: int | None = None


class CustomerResponse(BaseModel):
    customer_id: int
    phone_number: str
    full_name: str
    telegram_user_id: int | None = None

    class Config:
        from_attributes = True