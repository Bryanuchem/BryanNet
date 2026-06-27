from pydantic import BaseModel

from app.enums.session import NextAction

from app.schemas.customer import CustomerResponse


class SessionResponse(BaseModel):

    next_action: NextAction

    customer: CustomerResponse | None = None