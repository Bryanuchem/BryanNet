from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikInterfaceRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _interfaces(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "interface",

            )

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        interface_name,
    ):

        for interface in (

            MikroTikInterfaceRepository

            ._interfaces(

                api,

            )

        ):

            if (

                interface.get(

                    "name",

                )

                == interface_name

            ):

                return interface

        return None

    @staticmethod
    def get(
        api,
        interface_name,
    ):

        interface = (

            MikroTikInterfaceRepository

            .find(

                api,

                interface_name,

            )

        )

        if interface is None:

            raise ValueError(

                f"Interface "

                f"'{interface_name}' "

                "was not found."

            )

        return interface

    @staticmethod
    def get_all(
        api,
    ):

        return list(

            MikroTikInterfaceRepository

            ._interfaces(

                api,

            )

        )

    @staticmethod
    def get_statistics(
        api,
        interface_name,
    ):

        interface = (

            MikroTikInterfaceRepository

            .get(

                api,

                interface_name,

            )

        )

        return {

            "name": interface.get(
                "name",
            ),

            "running": interface.get(
                "running",
            ),

            "disabled": interface.get(
                "disabled",
            ),

            "last_link_up": interface.get(
                "last-link-up-time",
            ),

            "rx_bytes": interface.get(
                "rx-byte",
            ),

            "tx_bytes": interface.get(
                "tx-byte",
            ),

            "rx_packets": interface.get(
                "rx-packet",
            ),

            "tx_packets": interface.get(
                "tx-packet",
            ),

            "rx_errors": interface.get(
                "rx-error",
            ),

            "tx_errors": interface.get(
                "tx-error",
            ),

            "rx_drops": interface.get(
                "rx-drop",
            ),

            "tx_drops": interface.get(
                "tx-drop",
            ),

        }

    @staticmethod
    def get_all_statistics(
        api,
    ):

        return [

            (

                MikroTikInterfaceRepository

                .get_statistics(

                    api,

                    interface.get(

                        "name",

                    ),

                )

            )

            for interface in (

                MikroTikInterfaceRepository

                .get_all(

                    api,

                )

            )

        ]

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def enable(
        api,
        interface,
    ):

        if not interface.get(
            "disabled",
        ):

            return False

        (

            MikroTikInterfaceRepository

            ._interfaces(

                api,

            )

            .update(

                **{

                    ".id": interface[".id"],

                    "disabled": "no",

                },

            )

        )

        return True

    @staticmethod
    def disable(
        api,
        interface,
    ):

        if interface.get(
            "disabled",
        ):

            return False

        (

            MikroTikInterfaceRepository

            ._interfaces(

                api,

            )

            .update(

                **{

                    ".id": interface[".id"],

                    "disabled": "yes",

                },

            )

        )

        return True

    # ==========================================================
    # Convenience
    # ==========================================================

    @staticmethod
    def ensure(
        api,
        interface_name,
        enabled=True,
    ):

        interface = (

            MikroTikInterfaceRepository

            .get(

                api,

                interface_name,

            )

        )

        if enabled:

            return (

                MikroTikInterfaceRepository

                .enable(

                    api,

                    interface,

                )

            )

        return (

            MikroTikInterfaceRepository

            .disable(

                api,

                interface,

            )

        )