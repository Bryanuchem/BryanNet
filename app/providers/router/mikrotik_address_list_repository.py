from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikAddressListRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _address_lists(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "firewall",

                "address-list",

            )

        )

    @staticmethod
    def _to_address(
        address,
    ):

        return {

            "id": address.get(
                ".id",
            ),

            "list": address.get(
                "list",
            ),

            "address": address.get(
                "address",
            ),

            "comment": address.get(
                "comment",
            ),

            "disabled": address.get(
                "disabled",
            ),

            "dynamic": address.get(
                "dynamic",
            ),

            "creation_time": address.get(
                "creation-time",
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

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

        ):

            if (

                address.get(

                    ".id",

                )

                == address_id

            ):

                return (

                    MikroTikAddressListRepository

                    ._to_address(

                        address,

                    )

                )

        return None

    @staticmethod
    def find_by_list(
        api,
        list_name,
    ):

        for address in (

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

        ):

            if (

                address.get(

                    "list",

                )

                == list_name

            ):

                return (

                    MikroTikAddressListRepository

                    ._to_address(

                        address,

                    )

                )

        return None

    @staticmethod
    def find_by_address(
        api,
        address,
    ):

        for item in (

            MikroTikAddressListRepository

            ._address_lists(

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

                    MikroTikAddressListRepository

                    ._to_address(

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

            MikroTikAddressListRepository

            .find(

                api,

                address_id,

            )

        )

        if address is None:

            raise ValueError(

                f"Address list "

                f"'{address_id}' "

                "was not found."

            )

        return (

            MikroTikAddressListRepository

            ._to_address(

                address,

            )

        )

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikAddressListRepository

                ._to_address(

                    address,

                )

            )

            for address in (

                MikroTikAddressListRepository

                ._address_lists(

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
        list_name,
        address,
        comment=None,
    ):

        (

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

            .add(

                list=list_name,

                address=address,

                comment=comment,

            )

        )

    @staticmethod
    def rename(
        api,
        address_list,
        list_name,
    ):

        (

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

            .update(

                **{

                    ".id": address_list["id"],

                    "list": list_name,

                },

            )

        )

    @staticmethod
    def update(
        api,
        address_list,
        list_name,
        address,
        comment=None,
    ):

        (

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

            .update(

                **{

                    ".id": address_list["id"],

                    "list": list_name,

                    "address": address,

                    "comment": comment,

                },

            )

        )
        
    @staticmethod
    def delete(
        api,
        address_list,
    ):

        (

            MikroTikAddressListRepository

            ._address_lists(

                api,

            )

            .remove(

                address_list["id"],

            )

        )

    # ==========================================================
    # Convenience
    # ==========================================================
           
    @staticmethod
    def ensure(
        api,
        list_name,
        address,
        comment=None,
    ):

        address_list = (

            MikroTikAddressListRepository

            .find_by_address(

                api,

                address,

            )

        )

        if address_list is None:

            MikroTikAddressListRepository.create(

                api,

                list_name,

                address,

                comment,

            )

            return True

        changed = (

            address_list.get(

                "list",

            )

            != list_name

            or

            address_list.get(

                "comment",

            )

            != comment

        )

        if changed:

            MikroTikAddressListRepository.update(

                api,

                address_list,

                list_name,

                address,

                comment,

            )

            return True

        return False