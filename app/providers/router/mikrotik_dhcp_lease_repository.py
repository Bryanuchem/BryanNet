from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikDHCPLeaseRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _leases(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "dhcp-server",

                "lease",

            )

        )

    @staticmethod
    def _lease(
        lease,
    ):

        return {

            "id": lease.get(
                ".id",
            ),

            "address": lease.get(
                "address",
            ),

            "mac_address": lease.get(
                "mac-address",
            ),

            "hostname": lease.get(
                "host-name",
            ),

            "server": lease.get(
                "server",
            ),

            "status": lease.get(
                "status",
            ),

            "client_id": lease.get(
                "client-id",
            ),

            "class_id": lease.get(
                "class-id",
            ),

            "expires_after": lease.get(
                "expires-after",
            ),

            "last_seen": lease.get(
                "last-seen",
            ),

            "age": lease.get(
                "age",
            ),

            "active_address": lease.get(
                "active-address",
            ),

            "active_mac_address": lease.get(
                "active-mac-address",
            ),

            "active_client_id": lease.get(
                "active-client-id",
            ),

            "active_server": lease.get(
                "active-server",
            ),

            "address_lists": lease.get(
                "address-lists",
            ),

            "dhcp_option": lease.get(
                "dhcp-option",
            ),

            "radius": lease.get(
                "radius",
            ),

            "dynamic": lease.get(
                "dynamic",
            ),

            "blocked": lease.get(
                "blocked",
            ),

            "disabled": lease.get(
                "disabled",
            ),

            "comment": lease.get(
                "comment",
            ),

        }

    @staticmethod
    def _find(
        api,
        lease_id,
    ):

        for lease in (

            MikroTikDHCPLeaseRepository

            ._leases(

                api,

            )

        ):

            if (

                lease.get(

                    ".id",

                )

                == lease_id

            ):

                return lease

        return None

    @staticmethod
    def _get(
        api,
        lease_id,
    ):

        lease = (

            MikroTikDHCPLeaseRepository

            ._find(

                api,

                lease_id,

            )

        )

        if lease is None:

            raise ValueError(

                f"DHCP Lease "

                f"'{lease_id}' "

                "was not found."

            )

        return lease

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find_by_address(
        api,
        address,
    ):

        for lease in (

            MikroTikDHCPLeaseRepository

            ._leases(

                api,

            )

        ):

            if (

                lease.get(

                    "address",

                )

                == address

            ):

                return (

                    MikroTikDHCPLeaseRepository

                    ._lease(

                        lease,

                    )

                )

        return None

    @staticmethod
    def find_by_mac_address(
        api,
        mac_address,
    ):

        for lease in (

            MikroTikDHCPLeaseRepository

            ._leases(

                api,

            )

        ):

            if (

                lease.get(

                    "mac-address",

                )

                == mac_address

            ):

                return (

                    MikroTikDHCPLeaseRepository

                    ._lease(

                        lease,

                    )

                )

        return None

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikDHCPLeaseRepository

                ._lease(

                    lease,

                )

            )

            for lease in (

                MikroTikDHCPLeaseRepository

                ._leases(

                    api,

                )

            )

        ]

    @staticmethod
    def get(
        api,
        lease_id,
    ):

        return (

            MikroTikDHCPLeaseRepository

            ._lease(

                MikroTikDHCPLeaseRepository

                ._get(

                    api,

                    lease_id,

                )

            )

        )