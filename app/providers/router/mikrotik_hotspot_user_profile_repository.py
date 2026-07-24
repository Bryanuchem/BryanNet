from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikHotspotUserProfileRepository:

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

                "user",

                "profile",

            )

        )

    @staticmethod
    def rate_limit(
        speed_limit_mbps,
    ):

        return (

            f"{speed_limit_mbps}M/"

            f"{speed_limit_mbps}M"

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        profile_name,
    ):

        for profile in (

            MikroTikHotspotUserProfileRepository

            ._profiles(

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

    @staticmethod
    def ensure(
        api,
        profile_name,
        speed_limit,
        shared_users=1,
        on_login_script=None,
        on_logout_script=None,
    ):

        profile = (

            MikroTikHotspotUserProfileRepository

            .find(

                api,

                profile_name,

            )

        )

        desired_rate_limit = (

            MikroTikHotspotUserProfileRepository

            .rate_limit(

                speed_limit,

            )

        )

        payload = {

            "name": profile_name,

            "plan": type(

                "Plan",

                (),

                {

                    "speed_limit": desired_rate_limit,

                    "max_devices": shared_users,

                },

            )(),

            "on_login_script": on_login_script,
            "on_logout_script": on_logout_script,

        }

        if profile is None:

            (

                MikroTikHotspotUserProfileRepository

                .create(

                    api,

                    payload,

                )

            )

            return True

        changed = (

            profile.get(
                "rate-limit",
            )
            != desired_rate_limit

            or

            str(
                profile.get(
                    "shared-users",
                )
            )
            != str(
                shared_users,
            )

            or

            profile.get(
                "on-login",
                "",
            )
            != (
                on_login_script
                or ""
            )

            or

            profile.get(
                "on-logout",
                "",
            )
            != (
                on_logout_script
                or ""
            )

        )

        if changed:

            (

                MikroTikHotspotUserProfileRepository

                .update(

                    api,

                    profile,

                    payload,

                )

            )

        return changed

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        profile,
    ):

        plan = profile["plan"]

        (

            MikroTikHotspotUserProfileRepository

            ._profiles(

                api,

            )

            .add(

                name=profile["name"],

                **{

                    "shared-users": str(

                        plan.max_devices,

                    ),

                    "rate-limit": (

                        plan.speed_limit

                    ),

                    "on-login": (
                        
                        profile.get(
                            
                            "on_login_script"
                            
                        )
                        
                        or ""
                        
                    ),

                    "on-logout": (

                        profile.get(

                            "on_logout_script",

                        )

                        or ""

                    ),

                },

            )

        )

    @staticmethod
    def update(
        api,
        existing,
        profile,
    ):

        plan = profile["plan"]

        (

            MikroTikHotspotUserProfileRepository

            ._profiles(

                api,

            )

            .update(

                numbers=existing[".id"],

                **{

                    "shared-users": str(

                        plan.max_devices,

                    ),

                    "rate-limit": (

                        plan.speed_limit

                    ),

                    "on-login": (
                        
                        profile.get("on_login_script")
                        
                        or ""
                        
                    ),

                    "on-logout": (

                        profile.get(

                            "on_logout_script",

                        )

                        or ""

                    ),

                },

            )

        )
