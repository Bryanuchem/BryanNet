from pydantic import BaseModel


class PlanResponse(BaseModel):
    plan_id: int
    plan_name: str
    price: float
    duration_days: int
    speed_limit_mbps: int
    max_devices: int
    concurrent_devices: int

    class Config:
        from_attributes = True