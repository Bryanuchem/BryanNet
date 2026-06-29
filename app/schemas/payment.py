from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class PaymentBase(BaseModel):

    customer_id: int

    subscription_id: Optional[int] = None

    amount: Decimal

    payment_channel: str

    payment_method: Optional[str] = None

    status: str = "successful"

    notes: Optional[str] = None

    payment_date: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):

    payment_id: int

    customer_name: str

    phone_number: Optional[str] = None

    payment_reference: str

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True


class PaymentListItem(BaseModel):

    payment_id: int

    customer_id: int

    customer_name: str

    phone_number: Optional[str] = None

    subscription_id: Optional[int] = None

    amount: Decimal

    payment_channel: str

    payment_method: Optional[str] = None

    payment_reference: str

    status: str

    notes: Optional[str] = None

    payment_date: Optional[datetime] = None

    created_at: Optional[datetime] = None
    
    updated_at: Optional[datetime] = None

    class Config:

        from_attributes = True


class PaymentFilter(BaseModel):

    search: Optional[str] = None

    payment_channel: Optional[str] = None

    status: Optional[str] = None


class PaymentStatsResponse(BaseModel):

    total_payments: int

    total_revenue: Decimal

    successful_payments: int

    pending_payments: int

    failed_payments: int