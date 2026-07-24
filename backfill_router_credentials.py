import secrets

from app.database.database import (
    SessionLocal,
)

from app.models import (
    Router,
)


def main():

    db = SessionLocal()

    try:

        routers = (
            db.query(Router)
            .all()
        )

        print()

        print(
            f"Found {len(routers)} router(s)."
        )

        print()

        updated = 0

        for router in routers:

            changed = False

            if not router.router_identifier:

                router.router_identifier = (
                    f"ROUTER-{router.router_id:03d}"
                )

                changed = True

            if not router.router_secret:

                router.router_secret = (
                    secrets.token_urlsafe(48)
                )

                changed = True

            if changed:

                updated += 1

                print(
                    f"Updated Router {router.router_id}"
                )

        db.commit()

        print()

        print(
            "=" * 60
        )

        print(
            f"Updated {updated} router(s)."
        )

        print(
            "=" * 60
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":

    main()