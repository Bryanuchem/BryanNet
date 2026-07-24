from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikDHCPRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _servers(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "dhcp-server",

            )

        )

    @staticmethod
    def _networks(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "dhcp-server",

                "network",

            )

        )

    @staticmethod
    def _options(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "dhcp-server",

                "option",

            )

        )

    @staticmethod
    def _server(
        server,
    ):

        return {

            "id": server.get(
                ".id",
            ),

            "name": server.get(
                "name",
            ),

            "interface": server.get(
                "interface",
            ),

            "lease_time": server.get(
                "lease-time",
            ),

            "address_pool": server.get(
                "address-pool",
            ),

            "dynamic_lease_identifiers": server.get(
                "dynamic-lease-identifiers",
            ),

            "use_radius": server.get(
                "use-radius",
            ),

            "use_reconfigure": server.get(
                "use-reconfigure",
            ),

            "lease_script": server.get(
                "lease-script",
            ),

            "address_lists": server.get(
                "address-lists",
            ),

            "support_broadband_tr101": server.get(
                "support-broadband-tr101",
            ),

            "dynamic": server.get(
                "dynamic",
            ),

            "invalid": server.get(
                "invalid",
            ),

            "disabled": server.get(
                "disabled",
            ),

        }

    @staticmethod
    def _network(
        network,
    ):

        return {

            "id": network.get(
                ".id",
            ),

            "address": network.get(
                "address",
            ),

            "gateway": network.get(
                "gateway",
            ),

            "dns_server": network.get(
                "dns-server",
            ),

            "wins_server": network.get(
                "wins-server",
            ),

            "ntp_server": network.get(
                "ntp-server",
            ),

            "caps_manager": network.get(
                "caps-manager",
            ),

            "dhcp_option": network.get(
                "dhcp-option",
            ),

            "dynamic": network.get(
                "dynamic",
            ),

            "comment": network.get(
                "comment",
            ),

        }

    @staticmethod
    def _option(
        option,
    ):

        return {

            "id": option.get(
                ".id",
            ),

            "name": option.get(
                "name",
            ),

            "code": option.get(
                "code",
            ),

            "value": option.get(
                "value",
            ),

            "raw_value": option.get(
                "raw-value",
            ),

        }

    @staticmethod
    def _find(
        items,
        item_id,
    ):

        for item in items:

            if (

                item.get(

                    ".id",

                )

                == item_id

            ):

                return item

        return None

    @staticmethod
    def _get(
        items,
        item_id,
        label,
    ):

        item = (

            MikroTikDHCPRepository

            ._find(

                items,

                item_id,

            )

        )

        if item is None:

            raise ValueError(

                f"{label} "

                f"'{item_id}' "

                "was not found."

            )

        return item

    # ==========================================================
    # Query Methods
    # ==========================================================

    # ==========================================================
    # Find Helpers
    # ==========================================================

    @staticmethod
    def find_server_by_name(
        api,
        name,
    ):

        for server in (

            MikroTikDHCPRepository

            ._servers(

                api,

            )

        ):

            if (

                server.get(

                    "name",

                )

                == name

            ):

                return (

                    MikroTikDHCPRepository

                    ._server(

                        server,

                    )

                )

        return None

    @staticmethod
    def find_server_by_interface(
        api,
        interface,
    ):

        for server in (
            MikroTikDHCPRepository
            ._servers(api)
        ):

            if (
                server.get("interface")
                == interface
            ):

                return (
                    MikroTikDHCPRepository
                    ._server(server)
                )

        return None

    @staticmethod
    def find_network_by_address(
        api,
        address,
    ):

        for network in (

            MikroTikDHCPRepository

            ._networks(

                api,

            )

        ):

            if (

                network.get(

                    "address",

                )

                == address

            ):

                return (

                    MikroTikDHCPRepository

                    ._network(

                        network,

                    )

                )

        return None

    # ==========================================================
    # DHCP Servers
    # ==========================================================

    @staticmethod
    def get_servers(
        api,
    ):

        return [

            (

                MikroTikDHCPRepository

                ._server(

                    server,

                )

            )

            for server in (

                MikroTikDHCPRepository

                ._servers(

                    api,

                )

            )

        ]

    @staticmethod
    def get_server(
        api,
        server_id,
    ):

        return (

            MikroTikDHCPRepository

            ._server(

                MikroTikDHCPRepository

                ._get(

                    MikroTikDHCPRepository

                    ._servers(

                        api,

                    ),

                    server_id,

                    "DHCP Server",

                )

            )

        )

    # ==========================================================
    # DHCP Networks
    # ==========================================================

    @staticmethod
    def get_networks(
        api,
    ):

        return [

            (

                MikroTikDHCPRepository

                ._network(

                    network,

                )

            )

            for network in (

                MikroTikDHCPRepository

                ._networks(

                    api,

                )

            )

        ]

    @staticmethod
    def get_network(
        api,
        network_id,
    ):

        return (

            MikroTikDHCPRepository

            ._network(

                MikroTikDHCPRepository

                ._get(

                    MikroTikDHCPRepository

                    ._networks(

                        api,

                    ),

                    network_id,

                    "DHCP Network",

                )

            )

        )

    # ==========================================================
    # DHCP Options
    # ==========================================================

    @staticmethod
    def get_options(
        api,
    ):

        return [

            (

                MikroTikDHCPRepository

                ._option(

                    option,

                )

            )

            for option in (

                MikroTikDHCPRepository

                ._options(

                    api,

                )

            )

        ]

    @staticmethod
    def get_option(
        api,
        option_id,
    ):

        return (

            MikroTikDHCPRepository

            ._option(

                MikroTikDHCPRepository

                ._get(

                    MikroTikDHCPRepository

                    ._options(

                        api,

                    ),

                    option_id,

                    "DHCP Option",

                )

            )

        )
      
    # ==========================================================
    # Business Commands
    # ==========================================================
       
    @staticmethod
    def create_server(
        api,
        name,
        interface,
        address_pool,
        lease_time,
    ):

        (

            MikroTikDHCPRepository

            ._servers(

                api,

            )

            .add(

                name=name,

                interface=interface,

                **{

                    "address-pool": address_pool,

                    "lease-time": lease_time,

                },

            )
        )

    @staticmethod
    def rename_server(
        api,
        server,
        name,
    ):

        (

            MikroTikDHCPRepository

            ._servers(

                api,

            )

            .update(

                **{

                    ".id": server["id"],

                    "name": name,

                },

            )

        )

    @staticmethod
    def update_server(
        api,
        server,
        interface,
        address_pool,
        lease_time,
    ):

        (

            MikroTikDHCPRepository

            ._servers(

                api,

            )

            .update(

                **{

                    ".id": server["id"],

                    "interface": interface,

                    "address-pool": address_pool,

                    "lease-time": lease_time,

                }

            )

        )
    
    @staticmethod
    def delete_server(
        api,
        server,
    ):

        (

            MikroTikDHCPRepository

            ._servers(

                api,

            )

            .remove(

                server["id"],

            )

        )

    @staticmethod
    def create_network(
        api,
        address,
        gateway,
        dns_server,
        comment=None,
    ):

        (

            MikroTikDHCPRepository

            ._networks(

                api,

            )

            .add(
                
                address=address,
                
                gateway=gateway,
                
                **{
                    
                    "dns-server": dns_server,
                    
                },
                
                comment=comment,
                
            )

        )

    @staticmethod
    def update_network(
        api,
        network,
        gateway,
        dns_server,
        comment=None,
    ):

        (

            MikroTikDHCPRepository

            ._networks(

                api,

            )

            .update(

                **{

                    ".id": network["id"],

                    "gateway": gateway,

                    "dns-server": dns_server,

                    "comment": comment,

                }

            )

        )

    @staticmethod
    def delete_network(
        api,
        network,
    ):

        (

            MikroTikDHCPRepository

            ._networks(

                api,

            )

            .remove(

                network["id"],

            )

        )
        
    # ==========================================================
    # Convenience
    # ==========================================================
       
    @staticmethod
    def ensure_server(
        api,
        name,
        interface,
        address_pool,
        lease_time,
    ):

        server = (

            MikroTikDHCPRepository

            .find_server_by_name(

                api,

                name,

            )

        )

        if server is None:

            MikroTikDHCPRepository.create_server(

                api,

                name,

                interface,

                address_pool,

                lease_time,

            )

            return True

        changed = (

            server.get(
                "interface",
            )
            != interface

            or

            server.get(
                "address_pool",
            )
            != address_pool

            or

            server.get(
                "lease_time",
            )
            != lease_time

        )

        if changed:

            MikroTikDHCPRepository.update_server(

                api,

                server,

                interface,

                address_pool,

                lease_time,

            )

            return True

        return False

    @staticmethod
    def ensure_network(
        api,
        address,
        gateway,
        dns_server,
        comment=None,
    ):

        network = (

            MikroTikDHCPRepository

            .find_network_by_address(

                api,

                address,

            )

        )

        if network is None:

            MikroTikDHCPRepository.create_network(

                api,

                address,

                gateway,

                dns_server,

                comment,

            )

            return True

        changed = (

            network.get(

                "gateway",

            )

            != gateway

            or

            network.get(

                "dns_server",

            )

            != dns_server

            or

            network.get(

                "comment",

            )

            != comment

        )

        if changed:

            MikroTikDHCPRepository.update_network(

                api,

                network,

                gateway,

                dns_server,

                comment,

            )

            return True

        return False