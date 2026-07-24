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

    @staticmethod
    def _session(
        session,
    ):

        return {

            "id": session.get(
                ".id",
            ),

            "username": session.get(
                "name",
            ),

            "service": session.get(
                "service",
            ),

            "caller_id": session.get(
                "caller-id",
            ),

            "address": session.get(
                "address",
            ),

            "uptime": session.get(
                "uptime",
            ),

            "encoding": session.get(
                "encoding",
            ),

            "radius": session.get(
                "radius",
            ),

        }
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

        return [

            MikroTikSessionRepository._session(

                session,

            )

            for session in (

                MikroTikSessionRepository._active_sessions(

                    api,

                )

            )

        ]
        
    @staticmethod
    def get(
        api,
        username,
    ):

        session = (

            MikroTikSessionRepository.find(

                api,

                username,

            )

        )

        if session is None:

            raise ValueError(

                f"PPP Session "

                f"'{username}' "

                "was not found."

            )

        return (

            MikroTikSessionRepository._session(

                session,

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