from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
)


class PageRequest(BaseModel):

    page: Annotated[
        int,
        Field(
            ge=1,
        ),
    ] = 1

    page_size: Annotated[
        int,
        Field(
            ge=1,
            le=100,
        ),
    ] = 25