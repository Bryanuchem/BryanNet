from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikIPPoolRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _pools(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ip",

                "pool",

            )

        )

    @staticmethod
    def _to_pool(
        pool,
    ):

        return {

            "id": pool.get(
                ".id",
            ),

            "name": pool.get(
                "name",
            ),

            "ranges": pool.get(
                "ranges",
            ),

            "total": pool.get(
                "total",
            ),

            "used": pool.get(
                "used",
            ),

            "available": pool.get(
                "available",
            ),

            "comment": pool.get(
                "comment",
            ),

        }

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find_by_name(
        api,
        name,
    ):

        for pool in (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

        ):

            if (

                pool.get(

                    "name",

                )

                == name

            ):

                return (

                    MikroTikIPPoolRepository

                    ._to_pool(

                        pool,

                    )

                )

        return None

    @staticmethod
    def find(
        api,
        pool_id,
    ):

        for pool in (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

        ):

            if (

                pool.get(

                    ".id",

                )

                == pool_id

            ):

                return pool

        return None

    @staticmethod
    def get(
        api,
        pool_id,
    ):

        pool = (

            MikroTikIPPoolRepository

            .find(

                api,

                pool_id,

            )

        )

        if pool is None:

            raise ValueError(

                f"IP Pool "

                f"'{pool_id}' "

                "was not found."

            )

        return (

            MikroTikIPPoolRepository

            ._to_pool(

                pool,

            )

        )

    @staticmethod
    def get_all(
        api,
    ):

        return [

            (

                MikroTikIPPoolRepository

                ._to_pool(

                    pool,

                )

            )

            for pool in (

                MikroTikIPPoolRepository

                ._pools(

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
        name,
        ranges,
        comment=None,
    ):

        (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

            .add(

                name=name,

                ranges=ranges,

                comment=comment,

            )

        )

    @staticmethod
    def rename(
        api,
        pool,
        name,
    ):

        (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

            .update(

                **{

                    ".id": pool["id"],

                    "name": name,

                },

            )

        )

    @staticmethod
    def update(
        api,
        pool,
        name,
        ranges,
        comment=None,
    ):

        (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

            .update(

                **{

                    ".id": pool["id"],

                    "name": name,

                    "ranges": ranges,

                    "comment": comment,

                },

            )

        )

    @staticmethod
    def delete(
        api,
        pool,
    ):

        (

            MikroTikIPPoolRepository

            ._pools(

                api,

            )

            .remove(

                pool["id"],

            )

        )
        
    # ==========================================================
    # Convenience
    # ==========================================================
    
    @staticmethod
    def ensure(
        api,
        name,
        ranges,
        comment=None,
    ):

        pool = (

            MikroTikIPPoolRepository.find_by_name(

                api,

                name,

            )

        )

        if pool is None:

            MikroTikIPPoolRepository.create(

                api,

                name,

                ranges,

                comment,

            )

            return True

        changed = False

        if (

            pool.get(

                "ranges",

            )

            != ranges

        ):

            changed = True

        if (

            pool.get(

                "comment",

            )

            != comment

        ):

            changed = True

        if changed:

            MikroTikIPPoolRepository.update(

                api,

                pool,

                name,

                ranges,

                comment,

            )

            return True

        return False
