from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikProfileRepository:

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

                "ppp",

                "profile",

            )

        )

    # ==========================================================
    # Profile Naming
    # ==========================================================

    @staticmethod
    def profile_name(
        plan_id,
    ):

        return (

            f"BN_PLAN_{plan_id}"

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
        plan_id,
    ):

        profile_name = (

            MikroTikProfileRepository

            .profile_name(

                plan_id,

            )

        )

        for profile in (

            MikroTikProfileRepository

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
    def get_all(
        api,
    ):

        return list(

            MikroTikProfileRepository

            ._profiles(

                api,

            )

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        plan_id,
        speed_limit_mbps,
    ):

        (

            MikroTikProfileRepository

            ._profiles(

                api,

            )

            .add(

                name=(

                    MikroTikProfileRepository

                    .profile_name(

                        plan_id,

                    )

                ),

                **{

                    "rate-limit": (

                        MikroTikProfileRepository

                        .rate_limit(

                            speed_limit_mbps,

                        )

                    ),

                },

            )

        )

        return (

            MikroTikProfileRepository

            .profile_name(

                plan_id,

            )

        )

    @staticmethod
    def update(
        api,
        profile,
        speed_limit_mbps,
    ):

        (

            MikroTikProfileRepository

            ._profiles(

                api,

            )

            .update(

                **{

                    ".id": profile[".id"],

                    "rate-limit": (

                        MikroTikProfileRepository

                        .rate_limit(

                            speed_limit_mbps,

                        )

                    ),

                },

)

        )

        return profile.get(

            "name",

        )

    @staticmethod
    def ensure(
        api,
        plan_id,
        speed_limit_mbps,
    ):

        profile = (

            MikroTikProfileRepository

            .find(

                api,

                plan_id,

            )

        )

        if profile is None:

            return (

                MikroTikProfileRepository

                .create(

                    api,

                    plan_id,

                    speed_limit_mbps,

                )

            )

        return (

            MikroTikProfileRepository

            .update(

                api,

                profile,

                speed_limit_mbps,

            )

        )
        
    @staticmethod
    def delete(
        api,
        profile,
    ):

        (

            MikroTikProfileRepository

            ._profiles(

                api,

            )

            .remove(

                profile[".id"],

            )

        )

    @staticmethod
    def delete_orphans(
        api,
        active_plan_ids,
    ):

        active_profiles = {

            MikroTikProfileRepository

            .profile_name(

                plan_id,

            )

            for plan_id in active_plan_ids

        }

        deleted = 0

        for profile in (

            MikroTikProfileRepository

            .get_all(

                api,

            )

        ):

            profile_name = (

                profile.get(

                    "name",

                    "",

                )

            )

            if not profile_name.startswith(

                "BN_PLAN_",

            ):

                continue

            if profile_name in active_profiles:

                continue

            MikroTikProfileRepository.delete(

                api,

                profile,

            )

            deleted += 1

        return deleted