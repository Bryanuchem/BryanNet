from app.providers.router.mikrotik_connection import (
    MikroTikConnection,
)


class MikroTikSecretRepository:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _secrets(
        api,
    ):

        return (

            MikroTikConnection.path(

                api,

                "ppp",

                "secret",

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

        for secret in (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

        ):

            if (

                secret.get(

                    "name",

                )

                == username

            ):

                return secret

        return None

    @staticmethod
    def get_all(
        api,
    ):

        return list(

            MikroTikSecretRepository

            ._secrets(

                api,

            )

        )

    # ==========================================================
    # Business Commands
    # ==========================================================

    @staticmethod
    def create(
        api,
        username,
        password,
        profile,
        enabled=True,
    ):

        (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

            .add(

                name=username,

                password=password,

                profile=profile,

                disabled=(

                    "no"

                    if enabled

                    else "yes"

                ),

            )

        )

    @staticmethod
    def update(
        api,
        secret,
        password,
        profile,
    ):

        (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

            .update(

                **{

                    ".id": secret[".id"],

                    "password": password,

                    "profile": profile,

                }

            )

        )

    @staticmethod
    def enable(
        api,
        secret,
    ):

        (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

            .update(

                **{

                    ".id": secret[".id"],

                    "disabled": "no",

                }

            )

        )

    @staticmethod
    def disable(
        api,
        secret,
    ):

        (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

            .update(

                **{

                    ".id": secret[".id"],

                    "disabled": "yes",

                }

            )

        )

    @staticmethod
    def delete(
        api,
        secret,
    ):

        (

            MikroTikSecretRepository

            ._secrets(

                api,

            )

            .remove(

                secret[".id"],

            )

        )

    @staticmethod
    def ensure(
        api,
        username,
        password,
        profile,
        enabled=True,
    ):

        secret = (

            MikroTikSecretRepository

            .find(

                api,

                username,

            )

        )

        if secret is None:

            MikroTikSecretRepository.create(

                api,

                username,

                password,

                profile,

                enabled,

            )

            return (

                MikroTikSecretRepository

                .find(

                    api,

                    username,

                )

            )

        MikroTikSecretRepository.update(

            api,

            secret,

            password,

            profile,

        )

        secret = (

            MikroTikSecretRepository

            .find(

                api,

                username,

            )

        )

        if enabled:

            MikroTikSecretRepository.enable(

                api,

                secret,

            )

        else:

            MikroTikSecretRepository.disable(

                api,

                secret,

            )

        return (

            MikroTikSecretRepository

            .find(

                api,

                username,

            )

        )