from pydantic import BaseModel

from decimal import Decimal

from app.schemas.types import (
    PlanName,
    PositiveFloat,
    PositiveInt,
)


class PlanCreate(BaseModel):

    plan_name: PlanName

    price: Decimal

    duration_days: PositiveFloat

    speed_limit_mbps: PositiveInt

    max_devices: PositiveInt

    concurrent_devices: PositiveInt

    is_active: bool = True


class PlanResponse(BaseModel):

    plan_id: int

    plan_name: str

    price: Decimal

    duration_days: PositiveFloat

    speed_limit_mbps: int

    max_devices: int

    concurrent_devices: int

    is_active: bool

    class Config:

        from_attributes = True