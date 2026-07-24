from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikBackupRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _files(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "file",

            )

        )

    @staticmethod
    def _scheduler(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "system",

                "scheduler",

            )

        )

    @staticmethod
    def _file(
        file,
    ):

        return {

            "id": file.get(
                ".id",
            ),

            "name": file.get(
                "name",
            ),

            "type": file.get(
                "type",
            ),

            "size": file.get(
                "size",
            ),

            "last_modified": file.get(
                "last-modified",
            ),

        }

    @staticmethod
    def _schedule(
        schedule,
    ):

        return {

            "id": schedule.get(
                ".id",
            ),

            "name": schedule.get(
                "name",
            ),

            "start_date": schedule.get(
                "start-date",
            ),

            "start_time": schedule.get(
                "start-time",
            ),

            "interval": schedule.get(
                "interval",
            ),

            "next_run": schedule.get(
                "next-run",
            ),

            "run_count": schedule.get(
                "run-count",
            ),

            "disabled": schedule.get(
                "disabled",
            ),

            "comment": schedule.get(
                "comment",
            ),

        }

    @staticmethod
    def _find(
        resource,
        item_id,
    ):

        for item in resource:

            if (

                item.get(

                    ".id",

                )

                == item_id

            ):

                return item

        return None

    @staticmethod
    def _get(
        resource,
        item_id,
        resource_name,
    ):

        item = (

            MikroTikBackupRepository

            ._find(

                resource,

                item_id,

            )

        )

        if item is None:

            raise ValueError(

                f"{resource_name} "

                f"'{item_id}' "

                "was not found."

            )

        return item

    # ==========================================================
    # Files
    # ==========================================================

    @staticmethod
    def get_files(
        api,
    ):

        return [

            (

                MikroTikBackupRepository

                ._file(

                    file,

                )

            )

            for file in (

                MikroTikBackupRepository

                ._files(

                    api,

                )

            )

        ]

    @staticmethod
    def get_file(
        api,
        file_id,
    ):

        return (

            MikroTikBackupRepository

            ._file(

                MikroTikBackupRepository

                ._get(

                    MikroTikBackupRepository

                    ._files(

                        api,

                    ),

                    file_id,

                    "Router File",

                )

            )

        )

    # ==========================================================
    # Schedules
    # ==========================================================

    @staticmethod
    def get_schedules(
        api,
    ):

        return [

            (

                MikroTikBackupRepository

                ._schedule(

                    schedule,

                )

            )

            for schedule in (

                MikroTikBackupRepository

                ._scheduler(

                    api,

                )

            )

        ]

    @staticmethod
    def get_schedule(
        api,
        schedule_id,
    ):

        return (

            MikroTikBackupRepository

            ._schedule(

                MikroTikBackupRepository

                ._get(

                    MikroTikBackupRepository

                    ._scheduler(

                        api,

                    ),

                    schedule_id,

                    "Backup Schedule",

                )

            )

        )

    # ==========================================================
    # Commands
    # ==========================================================

    @staticmethod
    def create_backup(
        api,
        name,
    ):

        MikroTikConnection.path(

            api,

            "system",

            "backup",

        ).save(

            name=name,

        )

        return {

            "success": True,

            "message": "Backup created successfully.",

            "name": f"{name}.backup",

        }

    @staticmethod
    def create_export(
        api,
        name,
    ):

        MikroTikConnection.execute(

            api,

            "/export",

            file=name,

        )

        return {

            "success": True,

            "message": "Configuration exported successfully.",

            "name": f"{name}.rsc",

        }
        
