from app.providers.router.mikrotik_hotspot_user_profile_repository import (
    MikroTikHotspotUserProfileRepository,
)

from app.providers.router.mikrotik_hotspot_repository import (
    MikroTikHotspotRepository,
)

from app.routeros import (
    LOGIN_SCRIPT_NAME,
    LOGOUT_SCRIPT_NAME,
)


class RouterAccessService:

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def ensure_access(
        api,
        context,
    ):

        profile_name = f"BN-PLAN-{context.plan.plan_id}"

        MikroTikHotspotUserProfileRepository().ensure(

            api,

            profile_name=profile_name,

            speed_limit=context.plan.speed_limit_mbps,

            shared_users=context.plan.max_devices,

            on_login_script=LOGIN_SCRIPT_NAME,

            # RouterOS executes this named script when a customer
            # leaves the hotspot. The script sends the trusted
            # hotspot.logout event that closes BryanNet's lifecycle
            # session and updates the device's online state.
            on_logout_script=LOGOUT_SCRIPT_NAME,

        )

        # ======================================================
        # Normalize Router Usernames
        # ======================================================

        MikroTikHotspotRepository.normalize_usernames(

            api,

            context.router_account.username,

        )

        # ======================================================
        # Ensure Hotspot User
        # ======================================================

        user = (

            MikroTikHotspotRepository

            .ensure(

                api,

                username=(

                    context.router_account.username

                ),

                password=(

                    context.plaintext_password

                ),

                profile=profile_name,

                enabled=(

                    context.router_account.is_enabled

                ),

            )

        )

        # ======================================================
        # Enable / Disable
        # ======================================================

        if (

            context.router_account.is_enabled

        ):

            MikroTikHotspotRepository.enable(

                api,

                user,

            )

        else:

            MikroTikHotspotRepository.disable(

                api,

                user,

            )

        return user
