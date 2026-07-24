class MikroTikSchedulerRepository:

    # ==========================================================
    # Query Methods
    # ==========================================================

    def find(
        self,
        api,
        name,
    ):

        schedulers = api.path(

            "system",

            "scheduler",

        )

        return next(

            (

                scheduler

                for scheduler in schedulers

                if scheduler.get("name") == name

            ),

            None,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    def create(
        self,
        api,
        scheduler,
    ):

        api.path(

            "system",

            "scheduler",

        ).add(

            **scheduler,

        )

    def update(
        self,
        api,
        existing,
        scheduler,
    ):

        api.path(

            "system",

            "scheduler",

        ).update(

            numbers=existing[".id"],

            **scheduler,

        )