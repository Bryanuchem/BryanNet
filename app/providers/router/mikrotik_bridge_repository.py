from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikBridgeRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _bridges(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "interface/bridge",

            )

        )

    @staticmethod
    def _bridge_ports(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "interface/bridge/port",

            )

        )

    @staticmethod
    def _to_bridge(
        bridge,
    ):

        return {

            "id": bridge[".id"],

            "name": bridge["name"],

            "comment": bridge.get(

                "comment",

                "",

            ),

        }

    @staticmethod
    def _to_port(
        port,
    ):

        return {

            "id": port[".id"],

            "bridge": port["bridge"],

            "interface": port["interface"],

            "comment": port.get(

                "comment",

                "",

            ),

        }

    # ==========================================================
    # Bridge Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        bridge_name,
    ):

        for bridge in (

            MikroTikBridgeRepository

            ._bridges(

                api,

            )

        ):

            if (

                bridge.get(

                    "name",

                )

                == bridge_name

            ):

                return (

                    MikroTikBridgeRepository

                    ._to_bridge(

                        bridge,

                    )

                )

        return None

    @staticmethod
    def find_port(
        api,
        bridge_name,
        interface_name,
    ):

        for port in (

            MikroTikBridgeRepository

            ._bridge_ports(

                api,

            )

        ):

            if (

                port.get(

                    "bridge",

                )

                == bridge_name

                and

                port.get(

                    "interface",

                )

                == interface_name

            ):

                return (

                    MikroTikBridgeRepository

                    ._to_port(

                        port,

                    )

                )

        return None

    @staticmethod
    def find_port_by_interface(
        api,
        interface_name,
    ):

        for port in (

            MikroTikBridgeRepository

            ._bridge_ports(

                api,

            )

        ):

            if (

                port.get(

                    "interface",

                )

                == interface_name

            ):

                return (

                    MikroTikBridgeRepository

                    ._to_port(

                        port,

                    )

                )

        return None

    @staticmethod
    def get(
        api,
        bridge_name,
    ):

        bridge = (

            MikroTikBridgeRepository.find(

                api,

                bridge_name,

            )

        )

        if bridge is None:

            raise ValueError(

                f"Bridge "

                f"'{bridge_name}' "

                "was not found."

            )

        return bridge

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikBridgeRepository

                ._to_bridge(

                    bridge,

                )

            )

            for bridge in (

                MikroTikBridgeRepository

                ._bridges(

                    api,

                )

            )

        ]

    @staticmethod
    def get_ports(
        api,
        bridge_name,
    ):

        return [

            (

                MikroTikBridgeRepository

                ._to_port(

                    port,

                )

            )

            for port in (

                MikroTikBridgeRepository

                ._bridge_ports(

                    api,

                )

            )

            if (

                port.get(

                    "bridge",

                )

                == bridge_name

            )

        ]
 
    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        bridge_name,
    ):

        (

            MikroTikBridgeRepository

            ._bridges(

                api,

            )

            .add(

                name=bridge_name,

            )

        )

        return True

    @staticmethod
    def rename(
        api,
        bridge,
        bridge_name,
    ):

        return (

            MikroTikBridgeRepository

            .update(

                api,

                bridge,

                name=bridge_name,

            )

        )
        
    @staticmethod
    def update(
        api,
        bridge,
        **kwargs,
    ):

        (

            MikroTikBridgeRepository

            ._bridges(

                api,

            )

            .set(

                id=bridge["id"],

                **kwargs,

            )

        )

        return True

    @staticmethod
    def delete(
        api,
        bridge,
    ):

        (

            MikroTikBridgeRepository

            ._bridges(

                api,

            )

            .remove(

                bridge["id"],

            )

        )

        return True

    @staticmethod
    def add_port(
        api,
        bridge_name,
        interface_name,
    ):

        (

            MikroTikBridgeRepository

            ._bridge_ports(

                api,

            )

            .add(

                bridge=bridge_name,

                interface=interface_name,

            )

        )

        return True

    @staticmethod
    def update_port(
        api,
        port,
        **kwargs,
    ):

        (

            MikroTikBridgeRepository

            ._bridge_ports(

                api,

            )

            .set(

                id=port["id"],

                **kwargs,

            )

        )

        return True

    @staticmethod
    def remove_port(
        api,
        port,
    ):

        (

            MikroTikBridgeRepository

            ._bridge_ports(

                api,

            )

            .remove(

                port["id"],

            )

        )

        return True

    # ==========================================================
    # Convenience
    # ==========================================================

    @staticmethod
    def ensure(
        api,
        bridge_name,
    ):

        if (

            MikroTikBridgeRepository.find(

                api,

                bridge_name,

            )

            is not None

        ):

            return False

        MikroTikBridgeRepository.create(

            api,

            bridge_name,

        )

        return True
    
    @staticmethod
    def ensure_port(
        api,
        bridge_name,
        interface_name,
    ):

        if (

            MikroTikBridgeRepository.find_port(

                api,

                bridge_name,

                interface_name,

            )

            is not None

        ):

            return False

        MikroTikBridgeRepository.add_port(

            api,

            bridge_name,

            interface_name,

        )

        return True