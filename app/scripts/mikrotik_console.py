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

from app.providers.router.mikrotik_interface_repository import (
    MikroTikInterfaceRepository,
)

# ==========================================================
# Console Context
# ==========================================================

_console_context = None

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

    global _console_context

    if _console_context is not None:

        return _console_context

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

    _console_context = (

        router,

        provider,

    )

    return _console_context


def get_api(
    provider,
    router,
):

    if provider.api is None:

        provider.api = (

            provider.connection.connect(

                router,

            )

        )

    return provider.api


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

        "Interfaces",

    )

    print(

        "--------",

    )

    print(

        "12. List Interfaces",

    )

    print(

        "13. Interface Details",

    )
    
    print(

        "14. Enable Interface",

    )
    
    print(

        "15. Disable Interface",

    )

    print(

        "16. List Interface Statistics",

    )
    
    print(

        "17. Interface Statistics",

    )

    print()

    print(

        "Logs",

    )

    print(

        "--------",

    )

    print(

        "18. List Logs",

    )

    print(

        "19. Filter Logs",

    )
    
    print(

        "20. Search Logs",
    )

    print()

    print(

        "Address Lists",

    )

    print(

        "--------",

    )

    print(

        "21. List Address Lists",

    )

    print(

        "22. Address Details",

    )
    
    print(

        "23. Create Address List",
    )

    print(

        "24. Delete Address List",
    )

    print()

    print(

        "Firewall",

    )

    print(

        "--------",

    )

    print(

        "25. List Filter Rules",

    )

    print(

        "26. Filter Rule Details",

    )
    
    print(

        "27. List NAT Rules",
    )

    print(

        "28. NAT Rule Details",
    )

    print(

        "29. List Mangle Rules",

    )
    
    print(

        "30. Mangle Rule Details",
    )

    print(

        "31. List Raw Rules",
    )

    print(

        "32. Raw Rule Details",
    )

    print()

    print(

        "Queues",

    )

    print(

        "--------",

    )

    print(

        "33. List Simple Queues",

    )

    print(

        "34. Simple Queue Details",

    )
    
    print(

        "35. List Queue Trees",
    )

    print(

        "36. Queue Tree Details",
    )

    print()

    print(

        "IP Pools",

    )

    print(

        "--------",

    )

    print(

        "37. List IP Pools",

    )

    print(

        "38. Pool Details",

    )

    print(

        "39. Create IP Pool",

    )

    print(

        "40. Update IP Pool",

    )

    print(

        "41. Delete IP Pool",

    )

    print()

    print(

        "DHCP",

    )

    print(

        "--------",

    )
    print(

        "42. List DHCP Servers",

    )

    print(

        "43. DHCP Server Detailss",

    )

    print(

        "44. List DHCP Networks",

    )

    print(

        "45. DHCP Network Details",

    )

    print(

        "46. List DHCP Options",

    )

    print(

        "47. DHCP Option Details",

    )


    print()

    print(

        "DHCP Leases",

    )

    print(

        "--------",

    )
    
    print(

        "48. List DHCP Leases",

    )

    print(

        "49. DHCP Lease Details",

    )
    
    print()

    print(

        "Hotspot",

    )

    print(

        "--------",

    )
    
    print(

        "50. List Hotspot Profiles",

    )

    print(

        "51. Hotspot Profile Details",

    )

    print(

        "52. List Hotspot Servers",

    )

    print(

        "53. Hotspot Server Details",

    )

    print(

        "54. List Hotspot Users",

    )

    print(

        "55. Hotspot User Details",

    )
 
    print(

        "56. List Active Sessions",

    )

    print(

        "57. Active Session Details",
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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,


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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

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
            
            provider.persistent_connection,

        )


# ==========================================================
# Interface Commands
# ==========================================================

def list_interfaces(
    db,
    router_id,
):

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

        interfaces = (

            MikroTikInterfaceRepository

            .get_all(

                api,

            )

        )

        print()
        print("=" * 50)
        print("Interfaces")
        print("=" * 50)

        if not interfaces:

            print(
                "No interfaces found.",
            )

            return

        for interface in interfaces:

            print()

            print(
                f"Name      : {interface.get('name')}"
            )

            print(
                f"Type      : {interface.get('type')}"
            )

            print(
                f"Running   : {interface.get('running')}"
            )

            print(
                f"Disabled  : {interface.get('disabled')}"
            )

            print(
                "-" * 50,
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def interface_details(
    db,
    router_id,
):

    interface_name = input(
        "Interface Name: ",
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

        interface = (

            MikroTikInterfaceRepository

            .get(

                api,

                interface_name,

            )

        )

        print()
        print("=" * 50)
        print("Interface Details")
        print("=" * 50)

        for key, value in interface.items():

            print(
                f"{key:<20}: {value}"
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def enable_interface(
    db,
    router_id,
):

    interface_name = input(
        "Interface Name: ",
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

        try:

            interface = (

                MikroTikInterfaceRepository

                .get(

                    api,

                    interface_name,

                )

            )

        except ValueError as ex:

            print()

            print(str(ex))

            return

        changed = (

            MikroTikInterfaceRepository.enable(

                api,

                interface,

            )

        )

        print()

        if changed:

            print(
                "✓ Interface enabled.",
            )

        else:

            print(
                "Interface is already enabled.",
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def disable_interface(
    db,
    router_id,
):

    interface_name = input(
        "Interface Name: ",
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

        try:

            interface = (

                MikroTikInterfaceRepository

                .get(

                    api,

                    interface_name,

                )

            )

        except ValueError as ex:

            print()

            print(str(ex))

            return
        
        changed = (

            MikroTikInterfaceRepository.disable(

                api,

                interface,

            )

        )

        print()

        if changed:

            print(
                "✓ Interface disabled.",
            )

        else:

            print(
                "Interface is already disabled.",
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


# ==========================================================
# Interface Statistics
# ==========================================================

def list_interface_statistics(
    db,
    router_id,
):

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

        statistics = (

            MikroTikInterfaceRepository

            .get_all_statistics(

                api,

            )

        )

        print()
        print("=" * 60)
        print("Interface Statistics")
        print("=" * 60)

        for stat in statistics:

            print()

            for key, value in stat.items():

                print(
                    f"{key:<18}: {value}"
                )

            print("-" * 60)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def interface_statistics(
    db,
    router_id,
):

    interface_name = input(
        "Interface Name: ",
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

        statistics = (

            MikroTikInterfaceRepository

            .get_statistics(

                api,

                interface_name,

            )

        )

        print()
        print("=" * 60)
        print("Interface Statistics")
        print("=" * 60)

        for key, value in statistics.items():

            print(
                f"{key:<18}: {value}"
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


# ==========================================================
# Router Logs
# ==========================================================

def list_logs(
    db,
    router_id,
):

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

        logs = (

            provider.logs.get_all(

                api,

            )

        )

        print()
        print("=" * 80)
        print("Router Logs")
        print("=" * 80)

        for log in logs:

            print()

            for key, value in log.items():

                print(
                    f"{key:<15}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def filter_logs(
    db,
    router_id,
):

    print()
    print("1. Topic")
    print("2. Severity")
    print("3. Date")

    option = input(
        "Filter By: ",
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

        topic = None
        severity = None
        date = None

        if option == "1":

            topic = input(
                "Topic: ",
            )

        elif option == "2":

            severity = input(
                "Severity: ",
            )

        elif option == "3":

            date = input(
                "Date (YYYY-MM-DD): ",
            )

        else:

            print(
                "Invalid option.",
            )

            return

        logs = (

            provider.logs.filter(

                api,

                topic=topic,

                severity=severity,

                date=date,

            )

        )

        print()

        for log in logs:

            print(log)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def search_logs(
    db,
    router_id,
):

    text = input(
        "Search: ",
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

        logs = (

            provider.logs.filter(

                api,

                search=text,

            )

        )

        print()

        for log in logs:

            print(log)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# Address Lists
# ==========================================================

def list_address_lists(
    db,
    router_id,
):

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

        address_lists = (

            provider.address_lists.get_all(

                api,

            )

        )

        print()
        print("=" * 80)
        print("Address Lists")
        print("=" * 80)

        for address in address_lists:

            print()

            for key, value in address.items():

                print(
                    f"{key:<18}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def get_address_list(
    db,
    router_id,
):

    address_id = input(
        "Address ID: ",
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

        address = (

            provider.address_lists.get(

                api,

                address_id,

            )

        )

        print()
        print("=" * 80)
        print("Address List")
        print("=" * 80)

        for key, value in address.items():

            print(
                f"{key:<18}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def create_address_list(
    db,
    router_id,
):

    list_name = input(
        "List Name: ",
    )

    address = input(
        "Address: ",
    )

    comment = input(
        "Comment: ",
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

        provider.address_lists.create(

            api,

            list_name,

            address,

            comment or None,

        )

        print()
        print(
            "✓ Address list created."
        )

    finally:

        provider.connection.disconnect(
            
            api,
            
            
            provider.persistent_connection,

        )

def delete_address_list(
    db,
    router_id,
):

    address_id = input(
        "Address ID: ",
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

        provider.address_lists.delete(

            api,

            address_id,

        )

        print()
        print(
            "✓ Address list deleted."
        )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# Firewall
# ==========================================================

def list_firewall_rules(
    db,
    router_id,
    title,
    method_name,
):

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

        rules = getattr(

            provider.firewall,

            method_name,

        )(

            api,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for rule in rules:

            print()

            for key, value in rule.items():

                print(
                    f"{key:<24}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def firewall_rule_details(
    db,
    router_id,
    title,
    method_name,
):

    rule_id = input(
        "Rule ID: ",
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

        rule = getattr(

            provider.firewall,

            method_name,

        )(

            api,

            rule_id,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for key, value in rule.items():

            print(
                f"{key:<24}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# Queues
# ==========================================================

def list_queues(
    db,
    router_id,
    title,
    method_name,
):

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

        queues = getattr(

            provider.queues,

            method_name,

        )(

            api,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for queue in queues:

            print()

            for key, value in queue.items():

                print(
                    f"{key:<24}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def queue_details(
    db,
    router_id,
    title,
    method_name,
):

    queue_id = input(

        "Queue ID: ",

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

        queue = getattr(

            provider.queues,

            method_name,

        )(

            api,

            queue_id,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for key, value in queue.items():

            print(
                f"{key:<24}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# IP Pools
# ==========================================================

def list_ip_pools(
    db,
    router_id,
):

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

        pools = (

            provider.ip_pools.get_all(

                api,

            )

        )

        print()
        print("=" * 80)
        print("IP Pools")
        print("=" * 80)

        for pool in pools:

            print()

            for key, value in pool.items():

                print(
                    f"{key:<24}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def get_ip_pool(
    db,
    router_id,
):

    pool_id = input(

        "Pool ID: ",

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

        pool = (

            provider.ip_pools.get(

                api,

                pool_id,

            )

        )

        print()
        print("=" * 80)
        print("IP Pool")
        print("=" * 80)

        for key, value in pool.items():

            print(
                f"{key:<24}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def create_ip_pool(
    db,
    router_id,
):

    name = input(
        "Pool Name: ",
    )

    ranges = input(
        "Ranges: ",
    )

    comment = input(
        "Comment: ",
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

        provider.ip_pools.create(

            api,

            name,

            ranges,

            comment or None,

        )

        print()
        print(
            "✓ IP Pool created."
        )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def update_ip_pool(
    db,
    router_id,
):

    pool_id = input(
        "Pool ID: ",
    )

    name = input(
        "Pool Name: ",
    )

    ranges = input(
        "Ranges: ",
    )

    comment = input(
        "Comment: ",
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

        pool = (

            provider.ip_pools.find(

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

        provider.ip_pools.update(

            api,

            pool,

            name,

            ranges,

            comment or None,

        )

        print()
        print(
            "✓ IP Pool updated."
        )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def delete_ip_pool(
    db,
    router_id,
):

    pool_id = input(
        "Pool ID: ",
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

        pool = (

            provider.ip_pools.find(

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

        provider.ip_pools.delete(

            api,

            pool,

        )

        print()
        print(
            "✓ IP Pool deleted."
        )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# DHCP
# ==========================================================

def list_dhcp(
    db,
    router_id,
    title,
    method_name,
):

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

        items = getattr(

            provider.dhcp,

            method_name,

        )(

            api,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for item in items:

            print()

            for key, value in item.items():

                print(
                    f"{key:<24}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def dhcp_details(
    db,
    router_id,
    title,
    method_name,
    prompt,
):

    item_id = input(

        prompt,

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

        item = getattr(

            provider.dhcp,

            method_name,

        )(

            api,

            item_id,

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        for key, value in item.items():

            print(
                f"{key:<24}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# DHCP Leases
# ==========================================================

def list_dhcp_leases(
    db,
    router_id,
):

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

        leases = (

            provider.dhcp_leases.get_all(

                api,

            )

        )

        print()
        print("=" * 80)
        print("DHCP Leases")
        print("=" * 80)

        for lease in leases:

            print()

            for key, value in lease.items():

                print(
                    f"{key:<24}: {value}"
                )

            print("-" * 80)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def dhcp_lease_details(
    db,
    router_id,
):

    lease_id = input(

        "Lease ID: ",

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

        lease = (

            provider.dhcp_leases.get(

                api,

                lease_id,

            )

        )

        print()
        print("=" * 80)
        print("DHCP Lease")
        print("=" * 80)

        for key, value in lease.items():

            print(
                f"{key:<24}: {value}"
            )

    except ValueError as ex:

        print()
        print(ex)

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# Hotspot
# ==========================================================

def list_hotspot(
    db,
    router_id,
    title,
    method_name,
):

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

        items = (

            getattr(

                provider.hotspot,

                method_name,

            )(

                api,

            )

        )

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        found = False

        for item in items:

            found = True

            print(item)

        if not found:

            print()

            print(
                "No entries found."
            )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )


def hotspot_details(
    db,
    router_id,
    title,
    method_name,
    prompt,
):

    item_id = input(
        prompt,
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

        print()
        print("=" * 80)
        print(title)
        print("=" * 80)

        print(

            getattr(

                provider.hotspot,

                method_name,

            )(

                api,

                item_id,

            )

        )

    except ValueError as ex:

        print()

        print(
            ex,
        )

    finally:

        provider.connection.disconnect(
            
            api,
            
            provider.persistent_connection,

        )

# ==========================================================
# Business Commands
# ==========================================================

def synchronize_customer(
    db,
):

    from app.services.router_provisioning_service import (
        RouterProvisioningService,
    )

    customer_id = int(

        input(
            "Customer ID: ",
        )

    )

    result = (

        RouterProvisioningService

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
    
    provider = None

    global _console_context

    _console_context = None

    try:

        router_input = input(
            "Router ID [3]: ",
        ).strip()

        router_id = (

            int(router_input)

            if router_input

            else 3

        )

        router, provider = get_provider(

            db,

            router_id,

        )

        provider.persistent_connection = True

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

                case "12":
                    list_interfaces(
                        db,
                        router_id,
                    )

                case "13":
                    interface_details(
                        db,
                        router_id,
                    )

                case "14":
                    enable_interface(
                        db,
                        router_id,
                    )

                case "15":
                    disable_interface(
                        db,
                        router_id,
                    )

                case "16":
                    list_interface_statistics(
                        db,
                        router_id,
                    )

                case "17":
                    interface_statistics(
                        db,
                        router_id,
                    )

                case "18":
                    list_logs(
                        db,
                        router_id,
                    )

                case "19":
                    filter_logs(
                        db,
                        router_id,
                    )

                case "20":
                    search_logs(
                        db,
                        router_id,
                    )

                case "21":
                    list_address_lists(
                        db,
                        router_id,
                    )

                case "22":
                    get_address_list(
                        db,
                        router_id,
                    )

                case "23":
                    create_address_list(
                        db,
                        router_id,
                    )

                case "24":
                    delete_address_list(
                        db,
                        router_id,
                    )

                case "25":
                    list_firewall_rules(
                        db,
                        router_id,
                        "Filter Rules",
                        "get_filter_rules",
                    )

                case "26":
                    firewall_rule_details(
                        db,
                        router_id,
                        "Filter Rule",
                        "get_filter_rule",
                    )

                case "27":
                    list_firewall_rules(
                        db,
                        router_id,
                        "NAT Rules",
                        "get_nat_rules",
                    )

                case "28":
                    firewall_rule_details(
                        db,
                        router_id,
                        "NAT Rule",
                        "get_nat_rule",
                    )

                case "29":
                    list_firewall_rules(
                        db,
                        router_id,
                        "Mangle Rules",
                        "get_mangle_rules",
                    )

                case "30":
                    firewall_rule_details(
                        db,
                        router_id,
                        "Mangle Rule",
                        "get_mangle_rule",
                    )

                case "31":
                    list_firewall_rules(
                        db,
                        router_id,
                        "Raw Rules",
                        "get_raw_rules",
                    )

                case "32":
                    firewall_rule_details(
                        db,
                        router_id,
                        "Raw Rule",
                        "get_raw_rule",
                    )

                case "33":
                    list_queues(
                        db,
                        router_id,
                        "Simple Queues",
                        "get_simple_queues",
                    )

                case "34":
                    queue_details(
                        db,
                        router_id,
                        "Simple Queue",
                        "get_simple_queue",
                    )

                case "35":
                    list_queues(
                        db,
                        router_id,
                        "Queue Trees",
                        "get_queue_trees",
                    )

                case "36":
                    queue_details(
                        db,
                        router_id,
                        "Queue Tree",
                        "get_queue_tree",
                    )

                case "37":
                    list_ip_pools(
                        db,
                        router_id,
                    )

                case "38":
                    get_ip_pool(
                        db,
                        router_id,
                    )

                case "39":
                    create_ip_pool(
                        db,
                        router_id,
                    )

                case "40":
                    update_ip_pool(
                        db,
                        router_id,
                    )

                case "41":
                    delete_ip_pool(
                        db,
                        router_id,
                    )
                    
                case "42":

                    list_dhcp(
                        db,
                        router_id,
                        "DHCP Servers",
                        "get_servers",
                    )

                case "43":

                    dhcp_details(
                        db,
                        router_id,
                        "DHCP Server",
                        "get_server",
                        "Server ID: ",
                    )

                case "44":

                    list_dhcp(
                        db,
                        router_id,
                        "DHCP Networks",
                        "get_networks",
                    )

                case "45":

                    dhcp_details(
                        db,
                        router_id,
                        "DHCP Network",
                        "get_network",
                        "Network ID: ",
                    )

                case "46":

                    list_dhcp(
                        db,
                        router_id,
                        "DHCP Options",
                        "get_options",
                    )

                case "47":

                    dhcp_details(
                        db,
                        router_id,
                        "DHCP Option",
                        "get_option",
                        "Option ID: ",
                    )

                case "48":

                    list_dhcp_leases(
                        db,
                        router_id,
                    )

                case "49":

                    dhcp_lease_details(
                        db,
                        router_id,
                    )

                case "50":

                    list_hotspot(
                        db,
                        router_id,
                        "Hotspot Profiles",
                        "get_profiles",
                    )

                case "51":

                    hotspot_details(
                        db,
                        router_id,
                        "Hotspot Profile",
                        "get_profile",
                        "Profile ID: ",
                    )

                case "52":

                    list_hotspot(
                        db,
                        router_id,
                        "Hotspot Servers",
                        "get_servers",
                    )

                case "53":

                    hotspot_details(
                        db,
                        router_id,
                        "Hotspot Server",
                        "get_server",
                        "Server ID: ",
                    )

                case "54":

                    list_hotspot(
                        db,
                        router_id,
                        "Hotspot Users",
                        "get_users",
                    )

                case "55":

                    hotspot_details(
                        db,
                        router_id,
                        "Hotspot User",
                        "get_user",
                        "User ID: ",
                    )

                case "56":

                    list_hotspot(
                        db,
                        router_id,
                        "Hotspot Active",
                        "get_active",
                    )

                case "57":

                    hotspot_details(
                        db,
                        router_id,
                        "Hotspot Active Session",
                        "get_active_session",
                        "Session ID: ",
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

        if provider is not None:

            provider.connection.disconnect(

                provider.api,

                False,

            )

            provider.api = None

        _console_context = None

        db.close()


if __name__ == "__main__":

    main()