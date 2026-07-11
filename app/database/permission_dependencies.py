from fastapi import (
    Depends,
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.dependencies import (
    get_current_admin,
    get_db,
)

from app.services.permission_service import (
    PermissionService,
)


def require_permission(
    permission_key: str,
):

    def permission_dependency(

        db: Session = Depends(
            get_db,
        ),

        admin=Depends(
            get_current_admin,
        ),

    ):

        if not (

            PermissionService
            .has_permission(

                db=db,

                admin_id=admin.admin_user_id,

                permission_key=permission_key,

            )

        ):

            raise HTTPException(

                status_code=403,

                detail=(
                    "You do not have permission to perform this action."
                ),

            )

        return

    return permission_dependency