from app.services.device_service import (
    DeviceService,
)


class DeviceRegistrationService:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def register_or_touch(
        db,
        *,
        customer,
        mac_address,
        device_name=None,
    ):

        device = (

            DeviceService

            .find_by_mac_address(

                db,

                mac_address,

            )

        )

        if device:

            return (

                DeviceService

                .touch_device(

                    db,

                    mac_address,

                )

            )

        return (

            DeviceService

            .register_device(

                db,

                customer.customer_id,
                
                admin_id=None,

                mac_address=mac_address,

                device_name=(

                    device_name

                    or

                    mac_address

                ),

            )

        )