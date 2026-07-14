import secrets
import string

from cryptography.fernet import Fernet

from app.core.settings import settings


class RouterCredentialManager:

    # ==========================================================
    # Private Helpers
    # ==========================================================

    @staticmethod
    def _cipher():

        if not settings.router_encryption_key:

            raise RuntimeError(

                "ROUTER_ENCRYPTION_KEY is not configured."

            )

        return Fernet(

            settings.router_encryption_key.encode()

        )

    # ==========================================================
    # Password Generation
    # ==========================================================

    @staticmethod
    def generate_password(
        length: int = 12,
    ):

        alphabet = (

            string.ascii_letters

            + string.digits

        )

        return "".join(

            secrets.choice(alphabet)

            for _ in range(length)

        )

    # ==========================================================
    # Encryption
    # ==========================================================

    @staticmethod
    def encrypt(
        password: str,
    ):

        return (

            RouterCredentialManager

            ._cipher()

            .encrypt(
                password.encode(),
            )

            .decode()

        )

    @staticmethod
    def decrypt(
        encrypted_password: str,
    ):

        return (

            RouterCredentialManager

            ._cipher()

            .decrypt(
                encrypted_password.encode(),
            )

            .decode()

        )

    # ==========================================================
    # Rotation
    # ==========================================================

    @staticmethod
    def rotate_password():

        return (

            RouterCredentialManager

            .generate_password()

        )