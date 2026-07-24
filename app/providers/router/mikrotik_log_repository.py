from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikLogRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _logs(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "log",

            )

        )

    @staticmethod
    def _to_log(
        log,
    ):

        topics = (

            log.get(

                "topics",

                "",

            )

            .split(",")

        )

        topic = (

            topics[0]

            if topics

            else None

        )

        severity = None

        for value in (

            "critical",

            "error",

            "warning",

            "info",

            "debug",

        ):

            if value in topics:

                severity = value

                break

        categories = [

            item

            for item in topics

            if item not in {

                topic,

                severity,

            }

        ]

        return {

            "id": log.get(
                ".id",
            ),

            "time": log.get(
                "time",
            ),

            "topic": topic,

            "severity": severity,

            "categories": categories,

            "message": log.get(
                "message",
            ),

            "extra_info": log.get(
                "extra-info",
            ),

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikLogRepository

                ._to_log(

                    log,

                )

            )

            for log in (

                MikroTikLogRepository

                ._logs(

                    api,

                )

            )

        ]

    @staticmethod
    def filter(
        api,
        topic=None,
        severity=None,
        date=None,
        search=None,
    ):

        logs = (

            MikroTikLogRepository.get_all(

                api,

            )

        )

        if topic:

            logs = [

                log

                for log in logs

                if log["topic"] == topic

            ]

        if severity:

            logs = [

                log

                for log in logs

                if log["severity"] == severity

            ]

        if date:

            logs = [

                log

                for log in logs

                if log["time"].startswith(

                    date,

                )

            ]

        if search:

            value = search.lower()

            logs = [

                log

                for log in logs

                if value in log["message"].lower()

            ]

        return logs

