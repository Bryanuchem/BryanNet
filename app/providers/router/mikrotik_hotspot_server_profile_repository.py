from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikHotspotServerProfileRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _profiles(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "hotspot",

                "profile",

            )

        )

    @staticmethod
    def _profile(
        profile,
    ):

        return {

            "id": profile.get(
                ".id",
            ),

            "name": profile.get(
                "name",
            ),

            "hotspot_address": profile.get(
                "hotspot-address",
            ),

            "dns_name": profile.get(
                "dns-name",
            ),

            "html_directory": profile.get(
                "html-directory",
            ),

            "login_by": profile.get(
                "login-by",
            ),

            "radius_interim_update": profile.get(
                "radius-interim-update",
            ),

            "idle_timeout": profile.get(
                "idle-timeout",
            ),

            "keepalive_timeout": profile.get(
                "keepalive-timeout",
            ),

            "status_autorefresh": profile.get(
                "status-autorefresh",
            ),

            "shared_users": profile.get(
                "shared-users",
            ),

        }
    
    @staticmethod
    def get_all(
        api,
    ):

        return [

            (
                MikroTikHotspotServerProfileRepository
                ._profile(
                    profile,
                )
            )

            for profile in (

                MikroTikHotspotServerProfileRepository
                ._profiles(
                    api,
                )

            )

        ]
    
    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        profile_name,
    ):

        for profile in (

            MikroTikHotspotServerProfileRepository

            .get_all(

                api,

            )

        ):

            if (

                profile.get(

                    "name",

                )

                == profile_name

            ):

                return profile

        return None

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        profile,
    ):

        (

            MikroTikHotspotServerProfileRepository

            ._profiles(

                api,

            )

            .add(

                name=profile["name"],

                **{

                    "hotspot-address": profile["hotspot-address"],

                    "dns-name": profile["dns-name"],

                    "html-directory": profile["html-directory"],

                    "login-by": profile["login-by"],

                },

            )

        )

    @staticmethod
    def update(
        api,
        existing,
        profile,
    ):

        (

            MikroTikHotspotServerProfileRepository

            ._profiles(

                api,

            )

            .update(

                **{

                    ".id": existing["id"],

                    "hotspot-address": profile["hotspot-address"],

                    "dns-name": profile["dns-name"],

                    "html-directory": profile["html-directory"],

                    "login-by": profile["login-by"],

                },

            )

        )
            
    @staticmethod
    def rename(
        api,
        existing,
        name,
    ):

        (

            MikroTikHotspotServerProfileRepository

            ._profiles(
                api,
            )

            .update(

                **{

                    ".id": existing["id"],

                    "name": name,

                },

            )

        )
        
    @staticmethod
    def delete(
        api,
        existing,
    ):

        (

            MikroTikHotspotServerProfileRepository

            ._profiles(
                api,
            )

            .remove(

                existing["id"],

            )

        )
        

    @staticmethod
    def ensure(
        api,
        profile_name,
        hotspot_address,
        dns_name="",
        html_directory="hotspot",
        login_by="http-chap,cookie",
    ):

        profile = (

            MikroTikHotspotServerProfileRepository

            .find(

                api,

                profile_name,

            )

        )

        payload = {

            "name": profile_name,

            "hotspot-address": hotspot_address,

            "dns-name": dns_name,

            "html-directory": html_directory,

            "login-by": login_by,

        }

        if profile is None:

            (

                MikroTikHotspotServerProfileRepository

                .create(

                    api,

                    payload,

                )

            )

            return True

        current_login_by = set(
            filter(
                None,
                profile.get(
                    "login_by",
                    "",
                ).split(
                    ",",
                ),
            ),
        )

        desired_login_by = set(
            filter(
                None,
                login_by.split(
                    ",",
                ),
            ),
        )

        changed = (

            profile.get(

                "name",

            )

            != profile_name

            or

            profile.get(

                "hotspot_address",

            )

            != hotspot_address

            or

            profile.get(

                "dns_name",

            )

            != dns_name

            or

            profile.get(

                "html_directory",

            )

            != html_directory

            or

            current_login_by

            !=

            desired_login_by

        )
        
        if changed:

            
            (

                MikroTikHotspotServerProfileRepository

                .update(

                    api,

                    profile,

                    payload,

                )

            )
    
        return changed