from pydantic import BaseModel

from app.enums.next_action import NextAction
from app.schemas.customer import CustomerResponse


class SessionResponse(BaseModel):

    next_action: NextAction

    message: str

    keyboard: str

    customer: CustomerResponse | None = None
