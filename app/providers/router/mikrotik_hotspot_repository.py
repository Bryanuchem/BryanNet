from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)

from app.services.router_username_service import (
    RouterUsernameService,
)


class MikroTikHotspotRepository:

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

                "hotspot",

            )

        )

    @staticmethod
    def _users(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "hotspot",

                "user",

            )

        )

    @staticmethod
    def _active(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "hotspot",

                "active",

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

            "address_pool": server.get(
                "address-pool",
            ),

            "profile": server.get(
                "profile",
            ),

            "idle_timeout": server.get(
                "idle-timeout",
            ),

            "keepalive_timeout": server.get(
                "keepalive-timeout",
            ),

            "login_timeout": server.get(
                "login-timeout",
            ),

            "addresses_per_mac": server.get(
                "addresses-per-mac",
            ),

            "proxy_status": server.get(
                "proxy-status",
            ),

            "https": server.get(
                "HTTPS",
            ),

            "invalid": server.get(
                "invalid",
            ),

            "disabled": server.get(
                "disabled",
            ),

        }

    @staticmethod
    def _user(
        user,
    ):

        return {

            "id": user.get(
                ".id",
            ),

            "server": user.get(
                "server",
            ),

            "name": user.get(
                "name",
            ),

            "profile": user.get(
                "profile",
            ),

            "uptime": user.get(
                "uptime",
            ),

            "bytes_in": user.get(
                "bytes-in",
            ),

            "bytes_out": user.get(
                "bytes-out",
            ),

            "packets_in": user.get(
                "packets-in",
            ),

            "packets_out": user.get(
                "packets-out",
            ),

            "dynamic": user.get(
                "dynamic",
            ),

            "disabled": user.get(
                "disabled",
            ),

            "comment": user.get(
                "comment",
            ),

        }

    @staticmethod
    def _active_session(
        session,
    ):

        return {

            "id": session.get(
                ".id",
            ),

            "user": session.get(
                "user",
            ),

            "address": session.get(
                "address",
            ),

            "mac_address": session.get(
                "mac-address",
            ),

            "login_by": session.get(
                "login-by",
            ),

            "uptime": session.get(
                "uptime",
            ),

            "idle_time": session.get(
                "idle-time",
            ),

            "bytes_in": session.get(
                "bytes-in",
            ),

            "bytes_out": session.get(
                "bytes-out",
            ),

            "packets_in": session.get(
                "packets-in",
            ),

            "packets_out": session.get(
                "packets-out",
            ),

        }

    @staticmethod
    def _find(
        resource,
        item_id,
    ):

        for item in resource:

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
        resource,
        item_id,
        resource_name,
    ):

        item = (

            MikroTikHotspotRepository

            ._find(

                resource,

                item_id,

            )

        )

        if item is None:

            raise ValueError(

                f"{resource_name} "

                f"'{item_id}' "

                "was not found."

            )

        return item

    # ==========================================================
    # Servers
    # ==========================================================

    @staticmethod
    def get_servers(
        api,
    ):

        return [

            MikroTikHotspotRepository._server(
                server,
            )

            for server in (

                MikroTikHotspotRepository._servers(
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

            MikroTikHotspotRepository._server(

                MikroTikHotspotRepository._get(

                    MikroTikHotspotRepository._servers(
                        api,
                    ),

                    server_id,

                    "Hotspot Server",

                )

            )

        )

    # ==========================================================
    # Users
    # ==========================================================

    @staticmethod
    def get_users(
        api,
    ):

        return [

            MikroTikHotspotRepository._user(
                user,
            )

            for user in (

                MikroTikHotspotRepository._users(
                    api,
                )

            )

        ]

    @staticmethod
    def get_user(
        api,
        user_id,
    ):

        return (

            MikroTikHotspotRepository._user(

                MikroTikHotspotRepository._get(

                    MikroTikHotspotRepository._users(
                        api,
                    ),

                    user_id,

                    "Hotspot User",

                )

            )

        )

    # ==========================================================
    # Hotspot User Provisioning
    # ==========================================================

    @staticmethod
    def find(
        api,
        username,
    ):

        router_username = (

            RouterUsernameService

            .to_router(

                username,

            )

        )

        for user in (

            MikroTikHotspotRepository

            ._users(

                api,

            )

        ):

            if (

                user.get(

                    "name",

                )

                == router_username

            ):

                return user

        return None


    @staticmethod
    def create(
        api,
        username,
        password,
        profile,
        enabled=True,
    ):

        print("Creating hotspot user...")

        MikroTikHotspotRepository._users(

            api,

        ).add(

        name=(

            RouterUsernameService

            .to_router(

                username,

            )

        ),

            password=password,

            profile=profile,

            disabled=not enabled,

        )

        return (

            MikroTikHotspotRepository.find(

                api,

                username,

            )

        )
        
    @staticmethod
    def update(
        api,
        user,
        password,
        profile,
        enabled,
    ):

        (

            MikroTikHotspotRepository

            ._users(

                api,

            )

            .update(

                **{

                    ".id": user[".id"],

                    "password": password,

                    "profile": profile,

                    "disabled": not enabled,

                },

            )

        )

        return (

            MikroTikHotspotRepository.find(

                api,

                user["name"],

            )

        )

    @staticmethod
    def enable(
        api,
        user,
    ):

        if isinstance(

            user,

            str,

        ):

            user = (

                MikroTikHotspotRepository.find(

                    api,

                    user,

                )

            )

        if user is None:

            return

        MikroTikHotspotRepository._users(

            api,

        ).update(

            **{

                ".id": user[".id"],

                "disabled": "no",

            }

        )


    @staticmethod
    def disable(
        api,
        user,
    ):

        if isinstance(

            user,

            str,

        ):

            user = (

                MikroTikHotspotRepository.find(

                    api,

                    user,

                )

            )

        if user is None:

            return

        MikroTikHotspotRepository._users(

            api,

        ).update(

            **{

                ".id": user[".id"],

                "disabled": True,

            }

        )

    @staticmethod
    def ensure(
        api,
        username,
        password,
        profile,
        enabled=True,
    ):
        
        print("Entered hotspot.ensure")
        
        user = (

            MikroTikHotspotRepository.find(

                api,

                username,

            )

        )
        
        print(
            "Existing hotspot user:",
            user,
        )

        if user is None:

            user = (

                MikroTikHotspotRepository.create(

                    api,

                    username,

                    password,

                    profile,

                    enabled,

                )

            )

            print(
                "Created hotspot user:",
                user,
            )

        else:

            MikroTikHotspotRepository._users(

                api,

            ).update(

                **{

                ".id": user[".id"],

                "password": password,
                
                "profile": profile,

               "disabled": not enabled,
                
                }
            )

        print(
            "Returning hotspot user:",
            user,
        )

        return user

    # ==========================================================
    # Hotspot Server Provisioning
    # ==========================================================

    @staticmethod
    def find_server_by_name(
        api,
        name,
    ):

        for server in (

            MikroTikHotspotRepository

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

                    MikroTikHotspotRepository

                    ._server(

                        server,

                    )

                )

        return None

    @staticmethod
    def create_server(
        api,
        name,
        interface,
        profile,
        address_pool="none",
        idle_timeout="5m",
        keepalive_timeout="",
        login_timeout="",
        addresses_per_mac="2",
        disabled=False,
    ):

        (

            MikroTikHotspotRepository

            ._servers(

                api,

            )

            .add(

                name=name,

                interface=interface,

                profile=profile,

                **{

                    "address-pool": address_pool,

                    "idle-timeout": idle_timeout,

                    "keepalive-timeout": keepalive_timeout,

                    "login-timeout": login_timeout,

                    "addresses-per-mac": addresses_per_mac,

                    "disabled": disabled,

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

            MikroTikHotspotRepository

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
        name,
        interface,
        profile,
        address_pool="none",
        idle_timeout="5m",
        keepalive_timeout="",
        login_timeout="",
        addresses_per_mac="2",
        disabled=False,
    ):

        (

            MikroTikHotspotRepository

            ._servers(

                api,

            )

            .update(

                **{

                    ".id": server["id"],

                    "name": name,

                    "interface": interface,

                    "profile": profile,

                    "address-pool": address_pool,

                    "idle-timeout": idle_timeout,

                    "keepalive-timeout": keepalive_timeout,

                    "login-timeout": login_timeout,

                    "addresses-per-mac": addresses_per_mac,

                    "disabled": disabled,

                },

            )

        )

    @staticmethod
    def delete_server(
        api,
        server,
    ):

        (

            MikroTikHotspotRepository

            ._servers(

                api,

            )

            .remove(

                server["id"],

            )

        )
    
    @staticmethod
    def ensure_server(
        api,
        name,
        interface,
        profile,
        address_pool="none",
        idle_timeout="5m",
        keepalive_timeout="",
        login_timeout="",
        addresses_per_mac="2",
        disabled=False,
    ):

        server = (

            MikroTikHotspotRepository

            .find_server_by_name(

                api,

                name,

            )

        )

        if server is None:

            MikroTikHotspotRepository.create_server(

                api,

                name,

                interface,

                profile,

                address_pool,

                idle_timeout,

                keepalive_timeout,

                login_timeout,

                addresses_per_mac,

                disabled,

            )

            return True

        normalized_address_pool = (

            None

            if

            address_pool == "none"

            else

            address_pool

        )

        normalized_keepalive_timeout = (

            "none"

            if

            keepalive_timeout == ""

            else

            keepalive_timeout

        )

        normalized_login_timeout = (

            "none"

            if

            login_timeout == ""

            else

            login_timeout

        )

        normalized_addresses_per_mac = int(

            addresses_per_mac,

        )

        changed = (

            server.get(

                "name",

            )

            != name

            or

            server.get(

                "interface",

            )

            != interface

            or

            server.get(

                "profile",

            )

            != profile

            or

            server.get(

                "address_pool",

            )

            != normalized_address_pool

            or

            server.get(

                "idle_timeout",

            )

            != idle_timeout

            or

            server.get(

                "keepalive_timeout",

            )

            != normalized_keepalive_timeout

            or

            server.get(

                "login_timeout",

            )

            != normalized_login_timeout

            or

            server.get(

                "addresses_per_mac",

            )

            != normalized_addresses_per_mac

            or

            bool(

                server.get(

                    "disabled",

                )

            )

            != disabled

        )

        if changed:

            MikroTikHotspotRepository.update_server(

                api,

                server,

                name,

                interface,

                profile,

                address_pool,

                idle_timeout,

                keepalive_timeout,

                login_timeout,

                addresses_per_mac,

                disabled,

            )

        return changed

    # ==========================================================
    # Active Sessions
    # ==========================================================

    @staticmethod
    def get_active(
        api,
    ):

        return [

            MikroTikHotspotRepository._active_session(
                session,
            )

            for session in (

                MikroTikHotspotRepository._active(
                    api,
                )

            )

        ]

    @staticmethod
    def get_active_session(
        api,
        session_id,
    ):

        return (

            MikroTikHotspotRepository._active_session(

                MikroTikHotspotRepository._get(

                    MikroTikHotspotRepository._active(
                        api,
                    ),

                    session_id,

                    "Hotspot Active Session",

                )

            )

        )
        
    @staticmethod
    def delete(
        api,
        user,
    ):

        if isinstance(
            user,
            str,
        ):

            user = (

                MikroTikHotspotRepository.find(
                    api,
                    user,
                )

            )

        if user is None:

            return

        MikroTikHotspotRepository._users(
            api,
        ).remove(

            user[".id"],

        )
        
    @staticmethod
    def normalize_usernames(
        api,
        username,
    ):

        usernames = (

            RouterUsernameService

            .legacy_router_usernames(

                username,

            )

        )

        canonical = usernames[0]

        print("Canonical:", canonical)
        print("Legacy usernames:", usernames)

        for user in MikroTikHotspotRepository._users(api):

            name = user.get("name")

            print("Router user:", name)

            if name not in usernames:
                print("Skipping")
                continue

            print("Matched legacy:", name)

            if name == canonical:
                print("Already canonical")
                continue

            print("Deleting:", name)

            MikroTikHotspotRepository.delete(
                api,
                user,
            )