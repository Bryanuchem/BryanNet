from sqlalchemy.orm import Session

from app.models.router import Router
from app.schemas.router_event import RouterEventCreate

from app.services.customer_service import CustomerService

from app.services.router_username_service import (
    RouterUsernameService,
)

from app.services.router_account_service import (
    RouterAccountService,
)

from app.services.device_registration_service import (
    DeviceRegistrationService,
)

from app.services.router_events.session_tracking_service import (
    SessionTrackingService,
)
class HotspotLoginHandler:

    # ==========================================================
    # Public Methods
    # ==========================================================

    @staticmethod
    def process(
        db: Session,
        router: Router,
        request: RouterEventCreate,
    ):

        if request.username is None:

            return {

                "success": True,

            }

        username = (

            RouterUsernameService.from_router(

                request.username,

            )

        )

        router_account = (

            RouterAccountService

            .get_username_account(

                db,

                username,

            )

        )

        customer = (

            CustomerService.get_customer(

                db,

                router_account.customer_id,

            )

        )

        device = (

            DeviceRegistrationService

            .register_or_touch(

                db,

                customer=customer,

                mac_address=request.mac_address,

            )

        )

        SessionTrackingService.login(

            db,

            router_account=router_account,

            device=device,

            payload=request,

            session_type="hotspot",

        )

        RouterAccountService.mark_connected(

            db,

            router_account.router_account_id,

        )

        return {

            "success": True,

        }