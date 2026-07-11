import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

export default function PermissionGate({

    permission,

    any,

    all,

    fallback = null,

    children,

}) {

    const {

        loading,

        hasPermission,

        hasAnyPermission,

        hasAllPermissions,

    } = useCurrentPermissions();

    if (

        loading

    ) {

        return null;

    }

    let allowed = true;

    if (

        permission

    ) {

        allowed =

            hasPermission(

                permission,

            );

    }

    if (

        allowed &&

        any

    ) {

        allowed =

            hasAnyPermission(

                any,

            );

    }

    if (

        allowed &&

        all

    ) {

        allowed =

            hasAllPermissions(

                all,

            );

    }

    return allowed

        ? children

        : fallback;

}