from datetime import (
    datetime,
)

from sqlalchemy.orm import Session

from app.models.router import Router
from app.schemas.router_event import RouterEventCreate


from app.enums.router_status import (
    RouterStatus,
)

class RouterDailyCleanupHandler:

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def process(
        db: Session,
        router: Router,
        request: RouterEventCreate,
    ):

        return {

            "success": True,

        }