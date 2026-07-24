from __future__ import annotations

from app.providers.router.mikrotik_interface_repository import (
    MikroTikInterfaceRepository,
)

from app.providers.router.mikrotik_bridge_repository import (
    MikroTikBridgeRepository,
)

from app.providers.router.mikrotik_ip_address_repository import (
    MikroTikIPAddressRepository,
)

from app.providers.router.mikrotik_ip_pool_repository import (
    MikroTikIPPoolRepository,
)

from app.providers.router.mikrotik_dhcp_repository import (
    MikroTikDHCPRepository,
)

from app.providers.router.mikrotik_hotspot_server_profile_repository import (
    MikroTikHotspotServerProfileRepository,
)

from app.providers.router.mikrotik_hotspot_repository import (
    MikroTikHotspotRepository,
)

from app.providers.router.mikrotik_dns_repository import (
    MikroTikDNSRepository,
)

from app.providers.router.mikrotik_firewall_repository import (
    MikroTikFirewallRepository,
)

from app.providers.router.mikrotik_address_list_repository import (
    MikroTikAddressListRepository,
)

class HotspotDesiredStateService:

    # ==========================================================
    # Public API
    # ==========================================================
    
    @staticmethod
    def synchronize(
        api,
    ) -> dict:

        report = {

            "changed": [],

            "verified": [],

            "warnings": [],

            "errors": [],

            "actions": {},

        }

        pipeline = (

            (

                "interfaces",

                HotspotDesiredStateService.synchronize_interfaces,

            ),

            (

                "bridge",

                HotspotDesiredStateService.synchronize_bridge,

            ),
            
            (

                "ip_address",

                HotspotDesiredStateService.synchronize_ip_address,

            ),

            (

                "ip_pool",

                HotspotDesiredStateService.synchronize_ip_pool,

            ),

            (

                "dhcp",

                HotspotDesiredStateService.synchronize_dhcp,

            ),

            (

                "hotspot_server_profile",

                HotspotDesiredStateService.synchronize_hotspot_server_profile,

            ),

            (

                "hotspot_server",

                HotspotDesiredStateService.synchronize_hotspot_server,

            ),

            (

                "dns",

                HotspotDesiredStateService.synchronize_dns,

            ),

            (

                "nat",

                HotspotDesiredStateService.synchronize_nat,

            ),

            (

                "firewall",

                HotspotDesiredStateService.synchronize_firewall,

            ),

            (

                "address_lists",

                HotspotDesiredStateService.synchronize_address_lists,

            ),

            (

                "verification",

                HotspotDesiredStateService.verify_state,

            ),

        )

        for name, handler in pipeline:

            HotspotDesiredStateService._run(

                report,

                name,

                handler,

                api,

            )

        return report

    # ==========================================================
    # Internal
    # ==========================================================

    @staticmethod
    def _run(
        report,
        name,
        handler,
        api,
    ):

        try:

            result = handler(

                api,

            )

            if result is None:

                result = {

                    "status": "verified",

                }

            if isinstance(

                result,

                bool,

            ):

                result = {

                    "status": (

                        "changed"

                        if result

                        else "verified"

                    ),

                }

            report["actions"][

                name

            ] = result.get(

                "actions",

                [],

            )

            status = result.get(

                "status",

                "verified",

            )

            if status == "changed":

                report["changed"].append(

                    name,

                )

            elif status == "verified":

                report["verified"].append(

                    name,

                )

            elif status == "warning":

                report["warnings"].append(

                    {

                        "component": name,

                        "message": result.get(

                            "message",

                            "",

                        ),

                        "actions": result.get(

                            "actions",

                            [],

                        ),

                    }

                )

        except Exception as ex:

            report["errors"].append(

                {

                    "component": name,

                    "error": str(

                        ex,

                    ),

                    "actions": [],

                }

            )

    # ==========================================================
    # Synchronizers
    # ==========================================================

    @staticmethod
    def synchronize_interfaces(
        api,
    ):

        actions = []

        warnings = []

        desired = {

            "ether1": True,

            "ether2": True,

            "ether3": True,

        }

        # ==========================================================
        # Discover / Reconcile
        # ==========================================================

        for interface_name, enabled in desired.items():

            if (

                MikroTikInterfaceRepository

                .ensure(

                    api,

                    interface_name,

                    enabled,

                )

            ):

                actions.append(

                    f"Enabled interface '{interface_name}'."

                )

        # ==========================================================
        # Refresh
        # ==========================================================

        for interface_name in desired:

            interface = (

                MikroTikInterfaceRepository

                .get(

                    api,

                    interface_name,

                )

            )

            if not interface.get(

                "running",

            ):

                warnings.append(

                    f"{interface_name} is not running."

                )

        # ==========================================================
        # Report
        # ==========================================================

        if warnings:

            actions.extend(

                warnings,

            )

        return {

            "status": (

                "warning"

                if warnings

                else (

                    "changed"

                    if actions

                    else "verified"

                )

            ),

            "actions": actions,

        }

    @staticmethod
    def synchronize_bridge(
        api,
    ):

        actions = []

        interface_name = "ether3"

        # ==========================================================
        # Discover
        # ==========================================================

        port = (

            MikroTikBridgeRepository

            .find_port_by_interface(

                api,

                interface_name,

            )

        )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if port is not None:

            bridge = (

                MikroTikBridgeRepository

                .find(

                    api,

                    port["bridge"],

                )

            )

            MikroTikBridgeRepository.remove_port(

                api,

                port,

            )

            actions.append(

                f"Removed '{interface_name}' from bridge '{port['bridge']}'."

            )

        else:

            bridge = None

        # ==========================================================
        # Refresh
        # ==========================================================

        port = (

            MikroTikBridgeRepository

            .find_port_by_interface(

                api,

                interface_name,

            )

        )

        if port is not None:

            raise ValueError(

                f"Interface '{interface_name}' is still a bridge member."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        if bridge is not None:

            ports = (

                MikroTikBridgeRepository

                .get_ports(

                    api,

                    bridge["name"],

                )

            )

            if not ports:

                MikroTikBridgeRepository.delete(

                    api,

                    bridge,

                )

                actions.append(

                    f"Removed empty bridge '{bridge['name']}'."

                )

        # ==========================================================
        # Report
        # ==========================================================

        return {

            "status": (

                "changed"

                if actions

                else "verified"

            ),

            "actions": actions,

        }
                
    @staticmethod
    def synchronize_ip_address(
        api,
    ):

        actions = []

        changed = False

        desired = {

            "address": "10.10.10.1/24",

            "interface": "ether3",

            "comment": "BryanNet Hotspot",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        addresses = (

            MikroTikIPAddressRepository

            .get_all(

                api,

            )

        )

        if not addresses:

            MikroTikIPAddressRepository.ensure(

                api,

                **desired,

            )

            return {

                "status": "changed",

                "actions": [

                    "Created IP address.",

                ],

            }

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner = (

            MikroTikIPAddressRepository

            .find_by_interface(

                api,

                desired["interface"],

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner is None:

            owner = (

                MikroTikIPAddressRepository

                .find_by_address(

                    api,

                    desired["address"],

                )

            )

            if owner is not None:

                MikroTikIPAddressRepository.rename(

                    api,

                    owner,

                    desired["interface"],

                )

                changed = True

                actions.append(

                    "Adopted IP address."

                )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikIPAddressRepository

            .ensure(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled IP address.",

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        addresses = (

            MikroTikIPAddressRepository

            .get_all(

                api,

            )

        )

        owner = (

            MikroTikIPAddressRepository

            .find_by_interface(

                api,

                desired["interface"],

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile IP address."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for candidate in addresses:

            if candidate["id"] == owner["id"]:

                continue

            if (

                candidate.get(

                    "comment",

                    "",

                )

                == "BryanNet Hotspot"

            ):

                MikroTikIPAddressRepository.delete(

                    api,

                    candidate,

                )

                changed = True

                actions.append(

                    f"Removed duplicate IP address '{candidate['address']}'."

                )

                continue

            unmanaged.append(

                candidate["address"],

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged IP addresses: "

                + ", ".join(

                    unmanaged,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }

    @staticmethod
    def synchronize_ip_pool(
        api,
    ):

        actions = []

        changed = False

        desired = {

            "name": "bryannet_pool",

            "ranges": "10.10.10.10-10.10.10.254",

            "comment": "BryanNet Hotspot",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        pools = (

            MikroTikIPPoolRepository

            .get_all(

                api,

            )

        )

        if not pools:

            MikroTikIPPoolRepository.ensure(

                api,

                **desired,

            )

            return {

                "status": "changed",

                "actions": [

                    "Created IP pool.",

                ],

            }

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner = (

            MikroTikIPPoolRepository

            .find_by_name(

                api,

                desired["name"],

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner is None:

            for pool in pools:

                if (

                    pool.get(

                        "comment",

                    )

                    == "BryanNet Hotspot"

                ):

                    MikroTikIPPoolRepository.rename(

                        api,

                        pool,

                        desired["name"],

                    )

                    changed = True

                    actions.append(

                        "Adopted IP pool."

                    )

                    break

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikIPPoolRepository

            .ensure(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled IP pool.",

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        pools = (

            MikroTikIPPoolRepository

            .get_all(

                api,

            )

        )

        owner = (

            MikroTikIPPoolRepository

            .find_by_name(

                api,

                desired["name"],

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile IP pool."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for pool in pools:

            if pool["id"] == owner["id"]:

                continue

            if (

                pool.get(

                    "comment",

                    "",

                )

                == "BryanNet Hotspot"

            ):

                MikroTikIPPoolRepository.delete(

                    api,

                    pool,

                )

                changed = True

                actions.append(

                    f"Removed duplicate IP pool '{pool['name']}'."

                )

                continue

            unmanaged.append(

                pool["name"],

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged IP pools: "

                + ", ".join(

                    unmanaged,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_dhcp(
        api,
    ):

        actions = []

        changed = False

        # ==========================================================
        # Desired State
        # ==========================================================

        desired_server = {

            "name": "bryannet_dhcp",

            "interface": "ether3",

            "address_pool": "bryannet_pool",

            "lease_time": "1h",

        }

        desired_network = {

            "address": "10.10.10.0/24",

            "gateway": "10.10.10.1",

            "dns_server": "10.10.10.1",

            "comment": "BryanNet Hotspot",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        servers = (

            MikroTikDHCPRepository

            .get_servers(

                api,

            )

        )

        networks = (

            MikroTikDHCPRepository

            .get_networks(

                api,

            )

        )

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner_server = (

            MikroTikDHCPRepository

            .find_server_by_interface(

                api,

                desired_server["interface"],

            )

        )

        owner_network = (

            MikroTikDHCPRepository

            .find_network_by_address(

                api,

                desired_network["address"],

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner_server is not None:

            if (

                owner_server["name"]

                !=

                desired_server["name"]

            ):

                existing = (

                    MikroTikDHCPRepository

                    .find_server_by_name(

                        api,

                        desired_server["name"],

                    )

                )

                if (

                    existing is not None

                    and

                    existing["id"] != owner_server["id"]

                ):

                    MikroTikDHCPRepository.delete_server(

                        api,

                        existing,

                    )

                    changed = True

                    actions.append(

                        "Removed legacy DHCP server."

                    )

                MikroTikDHCPRepository.rename_server(

                    api,

                    owner_server,

                    desired_server["name"],

                )

                changed = True

                actions.append(

                    "Adopted DHCP server."

                )

                owner_server = (

                    MikroTikDHCPRepository

                    .find_server_by_name(

                        api,

                        desired_server["name"],

                    )

                )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikDHCPRepository

            .ensure_server(

                api,

                **desired_server,

            )

        ):

            changed = True

            actions.append(

                "Reconciled DHCP server.",

            )

        if (

            MikroTikDHCPRepository

            .ensure_network(

                api,

                **desired_network,

            )

        ):

            changed = True

            actions.append(

                "Reconciled DHCP network.",

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        servers = (

            MikroTikDHCPRepository

            .get_servers(

                api,

            )

        )

        networks = (

            MikroTikDHCPRepository

            .get_networks(

                api,

            )

        )

        owner_server = (

            MikroTikDHCPRepository

            .find_server_by_name(

                api,

                desired_server["name"],

            )

        )

        owner_network = (

            MikroTikDHCPRepository

            .find_network_by_address(

                api,

                desired_network["address"],

            )

        )

        if owner_server is None:

            raise ValueError(

                "Failed to reconcile DHCP server."

            )

        if owner_network is None:

            raise ValueError(

                "Failed to reconcile DHCP network."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged_servers = []

        for server in servers:

            if server["id"] == owner_server["id"]:

                continue

            if not server.get(

                "dynamic",

            ):

                MikroTikDHCPRepository.delete_server(

                    api,

                    server,

                )

                changed = True

                actions.append(

                    f"Removed duplicate DHCP server '{server['name']}'."

                )

                continue

            unmanaged_servers.append(

                server["name"],

            )

        unmanaged_networks = []

        for network in networks:

            if network["id"] == owner_network["id"]:

                continue

            if (

                network.get(

                    "comment",

                    "",

                )

                == "BryanNet Hotspot"

            ):

                MikroTikDHCPRepository.delete_network(

                    api,

                    network,

                )

                changed = True

                actions.append(

                    f"Removed duplicate DHCP network '{network['address']}'."

                )

                continue

            unmanaged_networks.append(

                network["address"],

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged_servers:

            actions.append(

                "Unmanaged DHCP servers: "

                + ", ".join(

                    unmanaged_servers,

                )

            )

        if unmanaged_networks:

            actions.append(

                "Unmanaged DHCP networks: "

                + ", ".join(

                    unmanaged_networks,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_hotspot_server_profile(
        api,
    ):

        actions = []

        changed = False

        desired_name = "bryannet_profile"

        desired = {

            "profile_name": desired_name,

            "hotspot_address": "10.10.10.1",

            "dns_name": "",

            "html_directory": "hotspot",

            "login_by": "http-chap,cookie",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        profiles = (

            MikroTikHotspotServerProfileRepository

            .get_all(

                api,

            )

        )

        if not profiles:

            MikroTikHotspotServerProfileRepository.ensure(

                api,

                **desired,

            )

            return {

                "status": "changed",

                "actions": [

                    "Created hotspot server profile.",

                ],

            }

        # ==========================================================
        # Select Owner
        # ==========================================================

        profile = (

            MikroTikHotspotServerProfileRepository

            .find(

                api,

                desired_name,

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if profile is None:

            profile = profiles[0]

            MikroTikHotspotServerProfileRepository.rename(

                api,

                profile,

                desired_name,

            )

            changed = True

            actions.append(

                f"Adopted '{profile['name']}'.",

            )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikHotspotServerProfileRepository

            .ensure(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled hotspot server profile.",

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        profiles = (

            MikroTikHotspotServerProfileRepository

            .get_all(

                api,

            )

        )

        owner = (

            MikroTikHotspotServerProfileRepository

            .find(

                api,

                desired_name,

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile hotspot server profile."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for candidate in profiles:

            if candidate["id"] == owner["id"]:

                continue

            name = candidate.get(

                "name",

                "",

            )

            lower = name.lower()

            if "bryannet" in lower:

                MikroTikHotspotServerProfileRepository.delete(

                    api,

                    candidate,

                )

                changed = True

                actions.append(

                    f"Removed duplicate '{name}'.",

                )

                continue

            unmanaged.append(

                name,

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged profiles: "

                + ", ".join(unmanaged)

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_hotspot_server(
        api,
    ):

        actions = []

        changed = False

        desired_name = "bryannet_hotspot"

        desired = {

            "name": desired_name,

            "interface": "ether3",

            "profile": "bryannet_profile",

            "address_pool": "none",

            "idle_timeout": "5m",

            "keepalive_timeout": "",

            "login_timeout": "",

            "addresses_per_mac": "2",

            "disabled": False,

        }

        # ==========================================================
        # Discover
        # ==========================================================

        servers = (

            MikroTikHotspotRepository

            .get_servers(

                api,

            )

        )

        if not servers:

            MikroTikHotspotRepository.ensure_server(

                api,

                **desired,

            )

            return {

                "status": "changed",

                "actions": [

                    "Created hotspot server.",

                ],

            }

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner = (

            MikroTikHotspotRepository

            .find_server_by_name(

                api,

                desired_name,

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner is None:

            MikroTikHotspotRepository.rename_server(

                api,

                servers[0],

                desired_name,

            )

            changed = True

            actions.append(

                f"Adopted hotspot server '{servers[0]['name']}'."

            )

            owner = (

                MikroTikHotspotRepository

                .find_server_by_name(

                    api,

                    desired_name,

                )

            )

            if owner is None:

                raise ValueError(

                    "Failed to adopt hotspot server."

                )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikHotspotRepository

            .ensure_server(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled hotspot server.",

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        servers = (

            MikroTikHotspotRepository

            .get_servers(

                api,

            )

        )

        owner = (

            MikroTikHotspotRepository

            .find_server_by_name(

                api,

                desired_name,

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile hotspot server."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for candidate in servers:

            if candidate["id"] == owner["id"]:

                continue

            name = candidate.get(

                "name",

                "",

            )

            if "bryannet" in name.lower():

                MikroTikHotspotRepository.delete_server(

                    api,

                    candidate,

                )

                changed = True

                actions.append(

                    f"Removed duplicate hotspot server '{name}'."

                )

                continue

            unmanaged.append(

                name,

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged hotspot servers: "

                + ", ".join(

                    unmanaged,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_dns(
        api,
    ):

        actions = []

        changed = False

        desired = {

            "servers": "1.1.1.1,8.8.8.8",

            "allow_remote_requests": True,

        }

        # ==========================================================
        # Discover
        # ==========================================================

        settings = (

            MikroTikDNSRepository

            .get(

                api,

            )

        )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikDNSRepository

            .ensure(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled DNS settings."

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        settings = (

            MikroTikDNSRepository

            .get(

                api,

            )

        )

        if settings is None:

            raise ValueError(

                "Failed to reconcile DNS settings."

            )

        # ==========================================================
        # Report
        # ==========================================================

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_nat(
        api,
    ):

        actions = []

        changed = False

        desired = {

            "chain": "srcnat",

            "action": "masquerade",

            "out_interface": "ether2",

            "comment": "BryanNet Internet",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        rules = (

            MikroTikFirewallRepository

            .get_nat_rules(

                api,

            )

        )

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner = (

            MikroTikFirewallRepository

            .find_nat_by_comment(

                api,

                desired["comment"],

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner is None:

            for rule in rules:

                if (

                    rule.get(

                        "action",

                    )

                    == "masquerade"

                ):

                    MikroTikFirewallRepository.rename_nat(

                        api,

                        rule,

                        desired["comment"],

                    )

                    changed = True

                    actions.append(

                        "Adopted NAT rule."

                    )

                    break

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikFirewallRepository

            .ensure_nat(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled NAT rule."

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        rules = (

            MikroTikFirewallRepository

            .get_nat_rules(

                api,

            )

        )

        owner = (

            MikroTikFirewallRepository

            .find_nat_by_comment(

                api,

                desired["comment"],

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile NAT rule."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for rule in rules:

            if rule["id"] == owner["id"]:

                continue

            if (

                rule.get(

                    "comment",

                    "",

                )

                == "BryanNet Internet"

            ):

                MikroTikFirewallRepository.delete_nat(

                    api,

                    rule,

                )

                changed = True

                actions.append(

                    "Removed duplicate NAT rule."

                )

                continue

            unmanaged.append(

                rule["chain"]

                + " -> "

                + rule["action"]

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged NAT rules: "

                + ", ".join(

                    unmanaged,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def synchronize_firewall(
        api,
    ):

        filter_rules = (

            MikroTikFirewallRepository

            .get_filter_rules(

                api,

            )

        )

        nat_rules = (

            MikroTikFirewallRepository

            .get_nat_rules(

                api,

            )

        )

        mangle_rules = (

            MikroTikFirewallRepository

            .get_mangle_rules(

                api,

            )

        )

        raw_rules = (

            MikroTikFirewallRepository

            .get_raw_rules(

                api,

            )

        )

        return {

            "status": "verified",

            "actions": [

                (

                    f"Verified "

                    f"{len(filter_rules)} "

                    "filter rule(s)."

                ),

                (

                    f"Verified "

                    f"{len(nat_rules)} "

                    "NAT rule(s)."

                ),

                (

                    f"Verified "

                    f"{len(mangle_rules)} "

                    "mangle rule(s)."

                ),

                (

                    f"Verified "

                    f"{len(raw_rules)} "

                    "raw rule(s)."

                ),

            ],

        }
        
    @staticmethod
    def synchronize_address_lists(
        api,
    ):

        actions = []

        changed = False

        desired = {

            "list_name": "bryannet_customers",

            "address": "10.10.10.0/24",

            "comment": "BryanNet Hotspot",

        }

        # ==========================================================
        # Discover
        # ==========================================================

        addresses = (

            MikroTikAddressListRepository

            .get_all(

                api,

            )

        )

        # ==========================================================
        # Select Owner
        # ==========================================================

        owner = (

            MikroTikAddressListRepository

            .find_by_list(

                api,

                desired["list_name"],

            )

        )

        # ==========================================================
        # Adopt
        # ==========================================================

        if owner is None:

            owner = (

                MikroTikAddressListRepository

                .find_by_address(

                    api,

                    desired["address"],

                )

            )

            if owner is not None:

                MikroTikAddressListRepository.rename(

                    api,

                    owner,

                    desired["list_name"],

                )

                changed = True

                actions.append(

                    "Adopted address list."

                )

        # ==========================================================
        # Reconcile
        # ==========================================================

        if (

            MikroTikAddressListRepository

            .ensure(

                api,

                **desired,

            )

        ):

            changed = True

            actions.append(

                "Reconciled address list."

            )

        # ==========================================================
        # Refresh
        # ==========================================================

        addresses = (

            MikroTikAddressListRepository

            .get_all(

                api,

            )

        )

        owner = (

            MikroTikAddressListRepository

            .find_by_list(

                api,

                desired["list_name"],

            )

        )

        if owner is None:

            raise ValueError(

                "Failed to reconcile address list."

            )

        # ==========================================================
        # Cleanup
        # ==========================================================

        unmanaged = []

        for address in addresses:

            if address["id"] == owner["id"]:

                continue

            if (

                address.get(

                    "comment",

                    "",

                )

                == "BryanNet Hotspot"

            ):

                MikroTikAddressListRepository.delete(

                    api,

                    address,

                )

                changed = True

                actions.append(

                    f"Removed duplicate address '{address['address']}'."

                )

                continue

            unmanaged.append(

                address["address"]

            )

        # ==========================================================
        # Report
        # ==========================================================

        if unmanaged:

            actions.append(

                "Unmanaged address list entries: "

                + ", ".join(

                    unmanaged,

                )

            )

        return {

            "status": (

                "changed"

                if changed

                else "verified"

            ),

            "actions": actions,

        }
        
    @staticmethod
    def verify_state(
        api,
    ):

        bridge_port = (

            MikroTikBridgeRepository

            .find_port_by_interface(

                api,

                "ether3",

            )

        )

        if bridge_port is not None:

            raise ValueError(

                "ether3 is still a bridge member."

            )

        ip_address = (

            MikroTikIPAddressRepository

            .find_by_address(

                api,

                "10.10.10.1/24",

            )

        )

        if ip_address is None:

            raise ValueError(

                "IP address '10.10.10.1/24' was not found."

            )

        if ip_address["interface"] != "ether3":

            raise ValueError(

                "IP address is assigned to the wrong interface."

            )

        ip_pool = (

            MikroTikIPPoolRepository

            .find_by_name(

                api,

                "bryannet_pool",

            )

        )

        if ip_pool is None:

            raise ValueError(

                "IP pool 'bryannet_pool' was not found."

            )

        if (

            ip_pool["ranges"]

            !=

            "10.10.10.10-10.10.10.254"

        ):

            raise ValueError(

                "IP pool range does not match the desired state."

            )

        dhcp_server = (

            MikroTikDHCPRepository

            .find_server_by_name(

                api,

                "bryannet_dhcp",

            )

        )

        if dhcp_server is None:

            raise ValueError(

                "DHCP server 'bryannet_dhcp' was not found."

            )

        if dhcp_server["interface"] != "ether3":

            raise ValueError(

                "DHCP server is assigned to the wrong interface."

            )

        if dhcp_server["address_pool"] != "bryannet_pool":

            raise ValueError(

                "DHCP server uses the wrong address pool."

            )

        dhcp_network = (

            MikroTikDHCPRepository

            .find_network_by_address(

                api,

                "10.10.10.0/24",

            )

        )

        if dhcp_network is None:

            raise ValueError(

                "DHCP network '10.10.10.0/24' was not found."

            )

        if dhcp_network["gateway"] != "10.10.10.1":

            raise ValueError(

                "DHCP gateway does not match the desired state."

            )

        if dhcp_network["dns_server"] != "10.10.10.1":

            raise ValueError(

                "DHCP DNS server does not match the desired state."

            )

        hotspot_profile = (

            MikroTikHotspotServerProfileRepository

            .find(

                api,

                "bryannet_profile",

            )

        )

        if hotspot_profile is None:

            raise ValueError(

                "Hotspot server profile 'bryannet_profile' was not found."

            )

        hotspot = (

            MikroTikHotspotRepository

            .find_server_by_name(

                api,

                "bryannet_hotspot",

            )

        )

        if hotspot is None:

            raise ValueError(

                "Hotspot server 'bryannet_hotspot' was not found."

            )

        if hotspot["interface"] != "ether3":

            raise ValueError(

                "Hotspot server is assigned to the wrong interface."

            )

        if hotspot["profile"] != "bryannet_profile":

            raise ValueError(

                "Hotspot server uses the wrong profile."

            )

        dns = (

            MikroTikDNSRepository

            .get(

                api,

            )

        )

        if dns["servers"] != "1.1.1.1,8.8.8.8":

            raise ValueError(

                "DNS servers do not match the desired state."

            )

        if not dns["allow_remote_requests"]:

            raise ValueError(

                "DNS remote requests are disabled."

            )

        nat = (

            MikroTikFirewallRepository

            .find_nat_by_comment(

                api,

                "BryanNet Internet",

            )

        )

        if nat is None:

            raise ValueError(

                "NAT rule 'BryanNet Internet' was not found."

            )

        if nat["chain"] != "srcnat":

            raise ValueError(

                "NAT rule uses the wrong chain."

            )

        if nat["action"] != "masquerade":

            raise ValueError(

                "NAT rule uses the wrong action."

            )

        if nat["out_interface"] != "ether2":

            raise ValueError(

                "NAT rule uses the wrong outbound interface."

            )

        address_list = (

            MikroTikAddressListRepository

            .find_by_list(

                api,

                "bryannet_customers",

            )

        )

        if address_list is None:

            raise ValueError(

                "Address list 'bryannet_customers' was not found."

            )

        if address_list["address"] != "10.10.10.0/24":

            raise ValueError(

                "Address list does not match the desired state."

            )

        return {

            "status": "verified",

        }