from librouteros import (
    connect,
)

from fastapi import (
    HTTPException,
)

from app.services.router_credential_manager import (
    RouterCredentialManager,
)


class MikroTikConnection:

    # ==========================================================
    # Connection
    # ==========================================================

    @staticmethod
    def connect(
        router,
    ):

        try:

            return connect(

                host=router.hostname,

                username=router.api_username,

                password=(

                    RouterCredentialManager.decrypt(

                        router.encrypted_api_password,

                    )

                ),

                port=router.api_port,

                timeout=router.connection_timeout,

            )

        except Exception as ex:

            raise HTTPException(

                status_code=503,

                detail=(

                    f"Unable to connect to router: {ex}"

                ),

            )

    @staticmethod
    def disconnect(
        api,
    ):

        if api is None:

            return

        try:

            api.close()

        except Exception:

            pass

    # ==========================================================
    # RouterOS Paths
    # ==========================================================

    @staticmethod
    def path(
        api,
        *parts,
    ):

        try:

            return api.path(
                *parts,
            )

        except Exception as ex:

            raise HTTPException(

                status_code=500,

                detail=(

                    f"Unable to access RouterOS path "
                    f"'{'/'.join(parts)}': {ex}"

                ),

            )