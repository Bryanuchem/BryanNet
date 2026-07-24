from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikIPAddressRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _addresses(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "address",

            )

        )

    @staticmethod
    def _address(
        address,
    ):

        return {

            "id": address.get(
                ".id",
            ),

            "address": address.get(
                "address",
            ),

            "network": address.get(
                "network",
            ),

            "interface": address.get(
                "interface",
            ),

            "dynamic": address.get(
                "dynamic",
            ),

            "disabled": address.get(
                "disabled",
            ),

            "comment": address.get(
                "comment",
            ),

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        address_id,
    ):

        for address in (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

        ):

            if (

                address.get(

                    ".id",

                )

                == address_id

            ):

                return address

        return None

    @staticmethod
    def find_by_address(
        api,
        address,
    ):

        for item in (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

        ):

            if (

                item.get(

                    "address",

                )

                == address

            ):

                return (

                    MikroTikIPAddressRepository

                    ._address(

                        item,

                    )

                )

        return None

    @staticmethod
    def find_by_interface(
        api,
        interface,
    ):

        for item in (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

        ):

            if (

                item.get(

                    "interface",

                )

                == interface

            ):
                
                return (

                    MikroTikIPAddressRepository

                    ._address(

                        item,

                    )

                )

        return None

    @staticmethod
    def get(
        api,
        address_id,
    ):

        address = (

            MikroTikIPAddressRepository

            .find(

                api,

                address_id,

            )

        )

        if address is None:

            raise ValueError(

                f"IP Address "

                f"'{address_id}' "

                "was not found."

            )

        return (

            MikroTikIPAddressRepository

            ._address(

                address,

            )

        )

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikIPAddressRepository

                ._address(

                    address,

                )

            )

            for address in (

                MikroTikIPAddressRepository

                ._addresses(

                    api,

                )

            )

        ]

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        address,
        interface,
        comment=None,
    ):

        (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

            .add(

                address=address,

                interface=interface,

                comment=comment,

            )

        )

    @staticmethod
    def rename(
        api,
        ip_address,
        interface,
    ):

        (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

            .update(

                **{

                    ".id": ip_address[".id"],

                    "interface": interface,

                },

            )

        )

    @staticmethod
    def update(
        api,
        ip_address,
        address,
        interface,
        comment=None,
    ):

        (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

            .update(

                **{

                    ".id": ip_address["id"],

                    "address": address,

                    "interface": interface,

                    "comment": comment,

                },

            )

        )

    @staticmethod
    def delete(
        api,
        ip_address,
    ):

        (

            MikroTikIPAddressRepository

            ._addresses(

                api,

            )

            .remove(

                ip_address["id"],

            )

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def ensure(
        api,
        address,
        interface,
        comment=None,
    ):

        ip_address = (

            MikroTikIPAddressRepository

            .find_by_interface(

                api,

                interface,

            )

        )

        if ip_address is None:

            MikroTikIPAddressRepository.create(

                api,

                address,

                interface,

                comment,

            )

            return True

        changed = (

            ip_address.get(

                "address",

            )

            != address

            or

            ip_address.get(

                "comment",

            )

            != comment

        )

        if changed:

            MikroTikIPAddressRepository.update(

                api,

                ip_address,

                address,

                interface,

                comment,

            )

            return True

        return False