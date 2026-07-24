from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikHotspotWalledGardenRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _rules(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "hotspot",

                "walled-garden",

                "ip",

            )

        )

    @staticmethod
    def _to_rule(
        rule,
    ):

        return {

            "id": rule.get(
                ".id",
            ),

            "dst_host": rule.get(
                "dst-host",
            ),

            "dst_port": rule.get(
                "dst-port",
            ),

            "protocol": rule.get(
                "protocol",
            ),

            "action": rule.get(
                "action",
            ),

            "disabled": rule.get(
                "disabled",
            ),

            "comment": rule.get(
                "comment",
            ),

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        dst_host,
        dst_port,
        protocol="tcp",
    ):

        for rule in (

            MikroTikHotspotWalledGardenRepository

            ._rules(

                api,

            )

        ):

            if (

                rule.get(

                    "dst-host",

                )

                == dst_host

                and

                str(

                    rule.get(

                        "dst-port",

                    )

                )

                == str(

                    dst_port,

                )

                and

                rule.get(

                    "protocol",

                )

                == protocol

            ):

                return rule

        return None

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikHotspotWalledGardenRepository

                ._to_rule(

                    rule,

                )

            )

            for rule in (

                MikroTikHotspotWalledGardenRepository

                ._rules(

                    api,

                )

            )

        ]

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        dst_host,
        dst_port,
        protocol="tcp",
        comment=None,
    ):

        (

            MikroTikHotspotWalledGardenRepository

            ._rules(

                api,

            )

            .add(

                action="accept",

                **{

                    "dst-host": dst_host,

                    "dst-port": str(
                        dst_port,
                    ),

                    "protocol": protocol,

                    "comment": comment,

                },

            )

        )

        return (

            MikroTikHotspotWalledGardenRepository

            .find(

                api,

                dst_host,

                dst_port,

                protocol,

            )

        )

    @staticmethod
    def ensure(
        api,
        dst_host,
        dst_port,
        protocol="tcp",
        comment=None,
    ):

        rule = (

            MikroTikHotspotWalledGardenRepository

            .find(

                api,

                dst_host,

                dst_port,

                protocol,

            )

        )

        if rule is not None:

            return rule

        return (

            MikroTikHotspotWalledGardenRepository

            .create(

                api,

                dst_host,

                dst_port,

                protocol,

                comment,

            )

        )

    @staticmethod
    def delete(
        api,
        rule,
    ):

        if isinstance(

            rule,

            str,

        ):

            rules = (

                MikroTikHotspotWalledGardenRepository

                ._rules(

                    api,

                )

            )

            for item in rules:

                if (

                    item.get(

                        ".id",

                    )

                    == rule

                ):

                    rule = item

                    break

            else:

                return

        if rule is None:

            return

        (

            MikroTikHotspotWalledGardenRepository

            ._rules(

                api,

            )

            .remove(

                rule[".id"],

            )

        )