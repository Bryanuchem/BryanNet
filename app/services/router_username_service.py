from app.core.settings import (
    settings,
)


class RouterUsernameService:

    # ==========================================================
    # Constants
    # ==========================================================

    PREFIX = (

        settings.router_username_prefix

    )

    # ==========================================================
    # Translation
    # ==========================================================

    @staticmethod
    def to_router_username(
        username: str,
    ):

        return (

            RouterUsernameService

            .from_router(

                username,

            )

        )

    @staticmethod
    def to_customer_username(
        username: str,
    ):

        return (

            RouterUsernameService

            .to_router(

                username,

            )

        )

    @staticmethod
    def to_router(
        username: str,
    ):

        if (

            username.startswith(

                RouterUsernameService.PREFIX,

            )

        ):

            return username[

                len(

                    RouterUsernameService.PREFIX,

                ):

            ]

        return username

    @staticmethod
    def from_router(
        username: str,
    ):

        if (

            username.startswith(

                RouterUsernameService.PREFIX,

            )

        ):

            return username

        return (

            f"{RouterUsernameService.PREFIX}"

            f"{username}"

        )
        
    @staticmethod
    def legacy_router_usernames(
        username: str,
    ):

        canonical = (

            RouterUsernameService.to_router(
                username,
            )

        )

        return list(

            dict.fromkeys(

                [

                    canonical,

                    RouterUsernameService.from_router(
                        canonical,
                    ),

                ]

            )

        )