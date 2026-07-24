class MikroTikScriptRepository:

    # ==========================================================
    # Query Methods
    # ==========================================================

    @staticmethod
    def find(
        api,
        name,
    ):

        scripts = api.path(

            "system",

            "script",

        )

        return next(

            (

                script

                for script in scripts

                if script.get("name") == name

            ),

            None,

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        *,
        name,
        source,
    ):

        api.path(

            "system",

            "script",

        ).add(

            name=name,

            source=source,

        )

    @staticmethod
    def update(
        api,
        existing,
        *,
        source,
    ):

        api.path(

            "system",

            "script",

        ).update(

            numbers=existing[".id"],

            source=source,

        )
            
    @staticmethod
    def ensure(
        api,
        *,
        name,
        source,
    ):

        existing = (

            MikroTikScriptRepository

            .find(

                api,

                name,

            )

        )

        if existing is None:

            MikroTikScriptRepository.create(

                api,

                name=name,

                source=source,

            )

            return True

        changed = (

            existing.get(

                "source",

            )

            != source

        )

        if changed:

            MikroTikScriptRepository.update(

                api,

                existing,

                source=source,

            )

        return changed