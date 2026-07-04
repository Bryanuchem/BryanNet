import getpass

from sqlalchemy import or_

from app.database.database import SessionLocal
from app.enums.admin_role import AdminRole
from app.models.admin_user import AdminUser
from app.utils.security import hash_password


def main():

    db = SessionLocal()

    try:

        username = input(
            "Username: ",
        ).strip()

        email = input(
            "Email: ",
        ).strip()

        password = getpass.getpass(
            "Password: ",
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

        print(
            "\nAvailable Roles:",
        )

        for role in AdminRole:

            print(
                f" - {role.value}",
            )

        role_input = input(
            "\nRole [SUPER_ADMIN]: ",
        ).strip()

        role = (

            AdminRole(
                role_input,
            )

            if role_input

            else AdminRole.SUPER_ADMIN

        )

        existing_admin = (

            db.query(
                AdminUser,
            )

            .filter(

                or_(

                    AdminUser.username == username,

                    AdminUser.email == email,

                )

            )

            .first()

        )

        if existing_admin:

            print(
                "\n❌ Username or email already exists.",
            )

            return

        admin = AdminUser(

            username=username,

            email=email,

            password_hash=hash_password(
                password,
            ),

            role=role,

        )

        db.add(
            admin,
        )

        db.commit()

        print(
            f"\n✅ Admin '{username}' created successfully.",
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