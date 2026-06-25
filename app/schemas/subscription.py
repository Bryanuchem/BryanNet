from pydantic import BaseModel
from datetime import datetime


class SubscriptionPurchase(BaseModel):
    customer_id: int
    plan_id: int


class SubscriptionResponse(BaseModel):
    subscription_id: int
    customer_id: int
    plan_id: int
    start_date: datetime
    expiry_date: datetime
    activation_sequence: int
    status: str

    class Config:
        from_attributes = True

class SubscriptionStatusResponse(BaseModel):
    plan_name: str | None = None
    status: str | None = None
    expiry_date: str | None = None
    queued_subscriptions: int      
    
