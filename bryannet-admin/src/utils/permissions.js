// ==========================================================
// Permission Helpers
// ==========================================================

export function hasPermission(

    permissions = [],

    permission,

) {

    if (

        !permission

    ) {

        return true;

    }

    return permissions.includes(

        permission,

    );

}

export function hasAnyPermission(

    permissions = [],

    requiredPermissions = [],

) {

    if (

        requiredPermissions.length === 0

    ) {

        return true;

    }

    return requiredPermissions.some(

        (

            permission,

        ) =>

            permissions.includes(

                permission,

            ),

    );

}

export function hasAllPermissions(

    permissions = [],

    requiredPermissions = [],

) {

    if (

        requiredPermissions.length === 0

    ) {

        return true;

    }

    return requiredPermissions.every(

        (

            permission,

        ) =>

            permissions.includes(

                permission,

            ),

    );

}