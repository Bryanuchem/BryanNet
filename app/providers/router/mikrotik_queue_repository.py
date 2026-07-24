from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikQueueRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _simple_queues(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "queue",

                "simple",

            )

        )

    @staticmethod
    def _queue_trees(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "queue",

                "tree",

            )

        )

    @staticmethod
    def _to_queue(
        queue,
        queue_type,
    ):

        data = {

            "id": queue.get(
                ".id",
            ),

            "queue_type": queue_type,

            "name": queue.get(
                "name",
            ),

            "parent": queue.get(
                "parent",
            ),

            "queue": queue.get(
                "queue",
            ),

            "comment": queue.get(
                "comment",
            ),

            "disabled": queue.get(
                "disabled",
            ),

            "invalid": queue.get(
                "invalid",
            ),

            "bytes": queue.get(
                "bytes",
            ),

            "packets": queue.get(
                "packets",
            ),

            "dropped": queue.get(
                "dropped",
            ),

            "rate": queue.get(
                "rate",
            ),

            "packet_rate": queue.get(
                "packet-rate",
            ),

            "queued_packets": queue.get(
                "queued-packets",
            ),

            "queued_bytes": queue.get(
                "queued-bytes",
            ),

            "limit_at": queue.get(
                "limit-at",
            ),

            "max_limit": queue.get(
                "max-limit",
            ),

            "burst_limit": queue.get(
                "burst-limit",
            ),

            "burst_threshold": queue.get(
                "burst-threshold",
            ),

            "burst_time": queue.get(
                "burst-time",
            ),

            "bucket_size": queue.get(
                "bucket-size",
            ),

        }

        optional_fields = {

            "target":
                "target",

            "packet-mark":
                "packet_mark",

            "packet-marks":
                "packet_marks",

            "priority":
                "priority",

            "total-bytes":
                "total_bytes",

            "total-packets":
                "total_packets",

            "total-dropped":
                "total_dropped",

            "total-rate":
                "total_rate",

            "total-packet-rate":
                "total_packet_rate",

            "total-queued-packets":
                "total_queued_packets",

            "total-queued-bytes":
                "total_queued_bytes",

        }

        for mikrotik_name, bryannet_name in (

            optional_fields.items()

        ):

            if mikrotik_name in queue:

                data[

                    bryannet_name

                ] = queue.get(

                    mikrotik_name,

                )

        return data

    @staticmethod
    def _find(
        resource,
        queue_id,
    ):

        for queue in resource:

            if (

                queue.get(

                    ".id",

                )

                == queue_id

            ):

                return queue

        return None

    @staticmethod
    def _get(
        resource,
        queue_type,
        queue_id,
    ):

        queue = (

            MikroTikQueueRepository

            ._find(

                resource,

                queue_id,

            )

        )

        if queue is None:

            raise ValueError(

                f"Queue "

                f"'{queue_id}' "

                "was not found."

            )

        return (

            MikroTikQueueRepository

            ._to_queue(

                queue,

                queue_type,

            )

        )

    @staticmethod
    def _get_all(
        resource,
        queue_type,
    ):

        return [

            (

                MikroTikQueueRepository

                ._to_queue(

                    queue,

                    queue_type,

                )

            )

            for queue in resource

        ]

    # ==========================================================
    # Simple Queues
    # ==========================================================

    @staticmethod
    def get_simple_queues(
        api,
    ):

        return (

            MikroTikQueueRepository

            ._get_all(

                MikroTikQueueRepository

                ._simple_queues(

                    api,

                ),

                "simple",

            )

        )

    @staticmethod
    def get_simple_queue(
        api,
        queue_id,
    ):

        return (

            MikroTikQueueRepository

            ._get(

                MikroTikQueueRepository

                ._simple_queues(

                    api,

                ),

                "simple",

                queue_id,

            )

        )

    # ==========================================================
    # Queue Trees
    # ==========================================================

    @staticmethod
    def get_queue_trees(
        api,
    ):

        return (

            MikroTikQueueRepository

            ._get_all(

                MikroTikQueueRepository

                ._queue_trees(

                    api,

                ),

                "tree",

            )

        )

    @staticmethod
    def get_queue_tree(
        api,
        queue_id,
    ):

        return (

            MikroTikQueueRepository

            ._get(

                MikroTikQueueRepository

                ._queue_trees(

                    api,

                ),

                "tree",

                queue_id,

            )

        )