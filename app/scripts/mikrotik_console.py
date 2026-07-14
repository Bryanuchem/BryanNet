from sqlalchemy.orm import (
    Session,
)

from app.database.database import (
    SessionLocal,
)

from app.providers.router.factory import (
    ProviderFactory,
)

from app.services.router_service import (
    RouterService,
)

from typing import cast

from app.providers.router.mikrotik_chr import (
    MikroTikCHRProvider,
)

from app.providers.router.mikrotik_profile_repository import (
    MikroTikProfileRepository,
)


# ==========================================================
# Database
# ==========================================================

def get_db():

    return SessionLocal()


# ==========================================================
# Router Helpers
# ==========================================================

def get_router(
    db: Session,
    router_id: int,
):

    return (

        RouterService.get_router(

            db,

            router_id,

        )

    )


def get_provider(
    db,
    router_id,
):

    router = get_router(
        db,
        router_id,
    )

    provider = cast(

        MikroTikCHRProvider,

        ProviderFactory.get(
            router,
        ),

    )

    return (
        router,
        provider,
    )


def get_api(
    provider,
    router,
):

    return (

        provider.connection.connect(

            router,

        )

    )


# ==========================================================
# Console
# ==========================================================

def clear_screen():

    print(

        "\n" * 5,

    )


def pause():

    input(

        "\nPress Enter to continue...",

    )


def print_header():

    clear_screen()

    print(

        "=" * 50,

    )

    print(

        " BryanNet MikroTik Development Console",

    )

    print(

        "=" * 50,

    )


def print_menu():

    print()

    print(

        "Router",

    )

    print(

        "------",

    )

    print(

        "1. Health Check",

    )

    print()

    print(

        "Profiles",

    )

    print(

        "--------",

    )

    print(

        "2. List Profiles",

    )

    print(

        "3. Ensure Profile",

    )

    print()

    print(

        "Secrets",

    )

    print(

        "-------",

    )

    print(

        "4. List Secrets",

    )

    print(

        "5. Ensure Secret",

    )

    print(

        "6. Enable Secret",

    )

    print(

        "7. Disable Secret",

    )

    print(

        "8. Delete Secret",

    )

    print()

    print(

        "Sessions",

    )

    print(

        "--------",

    )

    print(

        "9. List Active Sessions",

    )

    print(

        "10. Disconnect Session",

    )

    print()

    print(

        "Business",

    )

    print(

        "--------",

    )

    print(

        "11. Synchronize Customer",

    )

    print()

    print(

        "0. Exit",

    )

    print()


# ==========================================================
# Router Commands
# ==========================================================

def health_check(
    db,
    router_id,
):

    router, provider = (

        get_provider(

            db,

            router_id,

        )

    )

    health = (

        provider.health_check(

            router,

        )

    )

    print()

    print(

        "=" * 50,

    )

    print(

        "Health Check",

    )

    print(

        "=" * 50,

    )

    print(

        f"Healthy   : {health.healthy}",

    )

    print(

        f"Connected : {health.connected}",

    )

    print(

        f"Version   : {health.router_os_version}",

    )

    print(

        f"Latency   : {health.latency_ms} ms",

    )

    print(

        f"Message   : {health.message}",

    )


# ==========================================================
# Profile Commands
# ==========================================================

def list_profiles(
    db,
    router_id,
):

    router, provider = (

        get_provider(

            db,

            router_id,

        )

    )

    api = None

    try:

        api = (

            get_api(

                provider,

                router,

            )

        )

        profiles = (

            MikroTikProfileRepository

            .get_all(

                api,

            )

        )

        print()

        print(

            "=" * 50,

        )

        print(

            "PPP Profiles",

        )

        print(

            "=" * 50,

        )

        if not profiles:

            print(

                "No profiles found.",

            )

            return

        for profile in profiles:

            print()

            print(

                f"ID        : {profile.get('.id')}",

            )

            print(

                f"Name      : {profile.get('name')}",

            )

            print(

                f"Rate      : {profile.get('rate-limit')}",

            )

            print(

                "-" * 50,

            )

    finally:

        provider.connection.disconnect(
            api,
        )


def ensure_profile(
    db,
    router_id,
):

    from app.services.plan_service import (
        PlanService,
    )

    plan_id = int(

        input(

            "Plan ID: ",

        )

    )

    plan = (

        PlanService.get_plan(

            db,

            plan_id,

        )

    )

    router, provider = (

        get_provider(

            db,

            router_id,

        )

    )

    api = None

    try:

        api = (

            get_api(

                provider,

                router,

            )

        )

        profile = (

            MikroTikProfileRepository

            .ensure(

                api,

                plan.plan_id,

                plan.speed_limit_mbps,

            )

        )

        print()

        print(

            "✓ Profile synchronized",

        )

        print()

        print(

            f"Profile : {profile}",

        )

        print(

            f"Rate    : "

            f"{plan.speed_limit_mbps}M/"

            f"{plan.speed_limit_mbps}M",

        )

    finally:

        provider.connection.disconnect(

            api,

        )
        
# ==========================================================
# Secret Commands
# ==========================================================

def list_secrets(
    db,
    router_id,
):

    from app.providers.router.mikrotik_secret_repository import (
        MikroTikSecretRepository,
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        secrets = (

            MikroTikSecretRepository

            .get_all(

                api,

            )

        )

        print()
        print("=" * 50)
        print("PPP Secrets")
        print("=" * 50)

        if not secrets:

            print("No secrets found.")
            return

        for secret in secrets:

            print()

            print(
                f"Username : {secret.get('name')}"
            )

            print(
                f"Profile  : {secret.get('profile')}"
            )

            print(
                f"Disabled : {secret.get('disabled')}"
            )

            print(
                "-" * 50,
            )

    finally:

        provider.connection.disconnect(
            api,
        )


def ensure_secret(
    db,
    router_id,
):

    from app.providers.router.mikrotik_secret_repository import (
        MikroTikSecretRepository,
    )

    username = input(
        "Username: ",
    )

    password = input(
        "Password: ",
    )

    plan_id = int(
        input(
            "Plan ID: ",
        )
    )

    enabled = (

        input(
            "Enabled (y/n): ",
        )
        .lower()
        .startswith("y")

    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        profile = (

            MikroTikProfileRepository

            .ensure(

                api,

                plan_id,

                10,

            )

        )

        MikroTikSecretRepository.ensure(

            api,

            username=username,

            password=password,

            profile=profile,

            enabled=enabled,

        )

        print()
        print(
            "✓ Secret synchronized.",
        )

    finally:

        provider.connection.disconnect(
            api,
        )


def enable_secret(
    db,
    router_id,
):

    from app.providers.router.mikrotik_secret_repository import (
        MikroTikSecretRepository,
    )

    username = input(
        "Username: ",
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        secret = (

            MikroTikSecretRepository.find(

                api,

                username,

            )

        )

        if not secret:

            print(
                "Secret not found.",
            )

            return

        MikroTikSecretRepository.enable(

            api,

            secret,

        )

        print(
            "✓ Secret enabled.",
        )

    finally:

        provider.connection.disconnect(
            api,
        )


def disable_secret(
    db,
    router_id,
):

    from app.providers.router.mikrotik_secret_repository import (
        MikroTikSecretRepository,
    )

    username = input(
        "Username: ",
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        secret = (

            MikroTikSecretRepository.find(

                api,

                username,

            )

        )

        if not secret:

            print(
                "Secret not found.",
            )

            return

        MikroTikSecretRepository.disable(

            api,

            secret,

        )

        print(
            "✓ Secret disabled.",
        )

    finally:

        provider.connection.disconnect(
            api,
        )


def delete_secret(
    db,
    router_id,
):

    from app.providers.router.mikrotik_secret_repository import (
        MikroTikSecretRepository,
    )

    username = input(
        "Username: ",
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        secret = (

            MikroTikSecretRepository.find(

                api,

                username,

            )

        )

        if not secret:

            print(
                "Secret not found.",
            )

            return

        MikroTikSecretRepository.delete(

            api,

            secret,

        )

        print(
            "✓ Secret deleted.",
        )

    finally:

        provider.connection.disconnect(
            api,
        )


# ==========================================================
# Session Commands
# ==========================================================

def list_sessions(
    db,
    router_id,
):

    from app.providers.router.mikrotik_session_repository import (
        MikroTikSessionRepository,
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        sessions = (

            MikroTikSessionRepository.get_all(

                api,

            )

        )

        print()
        print("=" * 50)
        print("PPP Active Sessions")
        print("=" * 50)

        if not sessions:

            print(
                "No active sessions.",
            )

            return

        for session in sessions:

            print()

            print(
                f"Username : {session.get('name')}"
            )

            print(
                f"Address  : {session.get('address')}"
            )

            print(
                "-" * 50,
            )

    finally:

        provider.connection.disconnect(
            api,
        )

def disconnect_session(
    db,
    router_id,
):

    from app.providers.router.mikrotik_session_repository import (
        MikroTikSessionRepository,
    )

    username = input(
        "Username: ",
    )

    router, provider = get_provider(
        db,
        router_id,
    )

    api = None

    try:

        api = get_api(
            provider,
            router,
        )

        disconnected = (

            MikroTikSessionRepository

            .disconnect_username(

                api,

                username,

            )

        )

        if disconnected:

            print(
                "✓ Session disconnected.",
            )

        else:

            print(
                "No active session.",
            )

    finally:

        provider.connection.disconnect(
            api,
        )


# ==========================================================
# Business Commands
# ==========================================================

def synchronize_customer(
    db,
):

    from app.services.router_account_service import (
        RouterAccountService,
    )

    customer_id = int(

        input(
            "Customer ID: ",
        )

    )

    result = (

        RouterAccountService

        .synchronize_customer_access(

            db,

            customer_id,

        )

    )

    print()
    print(result)


# ==========================================================
# Entry Point
# ==========================================================

def main():

    db = get_db()

    try:

        router_input = input(
            "Router ID [3]: ",
        ).strip()

        router_id = (

            int(router_input)

            if router_input

            else 3

        )

        while True:

            print_header()

            print_menu()

            choice = input(
                "Select Option: ",
            ).strip()

            match choice:

                case "1":
                    health_check(
                        db,
                        router_id,
                    )

                case "2":
                    list_profiles(
                        db,
                        router_id,
                    )

                case "3":
                    ensure_profile(
                        db,
                        router_id,
                    )

                case "4":
                    list_secrets(
                        db,
                        router_id,
                    )

                case "5":
                    ensure_secret(
                        db,
                        router_id,
                    )

                case "6":
                    enable_secret(
                        db,
                        router_id,
                    )

                case "7":
                    disable_secret(
                        db,
                        router_id,
                    )

                case "8":
                    delete_secret(
                        db,
                        router_id,
                    )

                case "9":
                    list_sessions(
                        db,
                        router_id,
                    )

                case "10":
                    disconnect_session(
                        db,
                        router_id,
                    )

                case "11":
                    synchronize_customer(
                        db,
                    )

                case "0":

                    break

                case _:

                    print(
                        "Invalid option.",
                    )

            if choice != "0":

                pause()

    finally:

        db.close()


if __name__ == "__main__":

    main()