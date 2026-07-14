from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikSessionRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _active_sessions(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ppp",

                "active",

            )

        )

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        username,
    ):

        for session in (

            MikroTikSessionRepository

            ._active_sessions(

                api,

            )

        ):

            if (

                session.get(

                    "name",

                )

                == username

            ):

                return session

        return None

    @staticmethod
    def get_all(
        api,
    ):

        return list(

            MikroTikSessionRepository

            ._active_sessions(

                api,

            )

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def disconnect(
        api,
        session,
    ):

        if session is None:

            return False

        (

            MikroTikSessionRepository

            ._active_sessions(

                api,

            )

            .remove(

                session[".id"],

            )

        )

        return True

    @staticmethod
    def disconnect_username(
        api,
        username,
    ):

        session = (

            MikroTikSessionRepository

            .find(

                api,

                username,

            )

        )

        return (

            MikroTikSessionRepository

            .disconnect(

                api,

                session,

            )

        )

    @staticmethod
    def disconnect_all(
        api,
    ):

        disconnected = 0

        for session in (

            MikroTikSessionRepository

            .get_all(

                api,

            )

        ):

            (

                MikroTikSessionRepository

                .disconnect(

                    api,

                    session,

                )

            )

            disconnected += 1

        return disconnected