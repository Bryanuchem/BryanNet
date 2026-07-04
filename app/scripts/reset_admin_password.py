import getpass

from sqlalchemy import or_

from app.database.database import SessionLocal
from app.models.admin_user import AdminUser
from app.utils.security import hash_password


def main():

    db = SessionLocal()

    try:

        identifier = input(
            "Username or Email: ",
        ).strip()

        admin = (

            db.query(
                AdminUser,
            )

            .filter(

                or_(

                    AdminUser.username == identifier,

                    AdminUser.email == identifier,

                )

            )

            .first()

        )

        if admin is None:

            print(
                "\n❌ Admin not found.",
            )

            return

        password = getpass.getpass(
            "New Password: ",
        ).strip()

        confirm_password = getpass.getpass(
            "Confirm Password: ",
        ).strip()

        if password != confirm_password:

            print(
                "\n❌ Passwords do not match.",
            )

            return

        if len(password) < 8:

            print(
                "\n❌ Password must be at least 8 characters.",
            )

            return

        admin.password_hash = hash_password(password)  # pyright: ignore[reportAttributeAccessIssue]

        db.commit()

        print(
            f"\n✅ Password updated successfully for '{admin.username}'.",
        )

    except Exception as e:

        db.rollback()

        print(
            f"\n❌ Error: {e}",
        )

    finally:

        db.close()


if __name__ == "__main__":

    main()