from app.database.database import SessionLocal

from app.services.router_service import (
    RouterService,
)

db = SessionLocal()

try:

    health = RouterService.get_router_health(
        db,
        3,
    )

    print(health)

finally:

    db.close()