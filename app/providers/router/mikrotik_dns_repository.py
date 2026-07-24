from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikDNSRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _dns(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "dns",

            )

        )

    @staticmethod
    def _settings(
        settings,
    ):

        return {

            "servers": settings.get(
                "servers",
            ),

            "dynamic_servers": settings.get(
                "dynamic-servers",
            ),

            "allow_remote_requests": settings.get(
                "allow-remote-requests",
            ),

            "cache_size": settings.get(
                "cache-size",
            ),

            "cache_used": settings.get(
                "cache-used",
            ),

            "cache_max_ttl": settings.get(
                "cache-max-ttl",
            ),

            "max_udp_packet_size": settings.get(
                "max-udp-packet-size",
            ),

            "query_server_timeout": settings.get(
                "query-server-timeout",
            ),

            "query_total_timeout": settings.get(
                "query-total-timeout",
            ),

            "verify_doh_cert": settings.get(
                "verify-doh-cert",
            ),

            "use_doh_server": settings.get(
                "use-doh-server",
            ),

            "vrf": settings.get(
                "vrf",
            ),

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get(
        api,
    ):

        settings = next(

            iter(

                MikroTikDNSRepository

                ._dns(

                    api,

                )

            ),

            None,

        )

        if settings is None:

            raise ValueError(

                "DNS configuration was not found."

            )

        return (

            MikroTikDNSRepository

            ._settings(

                settings,

            )

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def update(
        api,
        servers,
        allow_remote_requests,
    ):

        (

            MikroTikDNSRepository

            ._dns(

                api,

            )

            .update(

                **{

                    "servers": servers,

                    "allow-remote-requests": allow_remote_requests,

                },

            )

        )

    # ==========================================================
    # Convenience
    # ==========================================================

    @staticmethod
    def ensure(
        api,
        servers,
        allow_remote_requests,
    ):

        settings = (

            MikroTikDNSRepository

            .get(

                api,

            )

        )

        changed = (

            settings.get(

                "servers",

            )

            != servers

            or

            settings.get(

                "allow_remote_requests",

            )

            != allow_remote_requests

        )

        if changed:

            MikroTikDNSRepository.update(

                api,

                servers,

                allow_remote_requests,

            )

            return True

        return False