from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class JobResultResponse(BaseModel):
    processed: int
    message: str