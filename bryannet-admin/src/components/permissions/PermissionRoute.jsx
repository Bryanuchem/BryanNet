import {

    Navigate,

    useLocation,

} from "react-router-dom";

import {

    useCurrentPermissions,

} from "../../hooks/useCurrentPermissions";

export default function PermissionRoute({

    permission,

    any,

    all,

    children,

}) {

    const {

        loading,

        hasPermission,

        hasAnyPermission,

        hasAllPermissions,

    } = useCurrentPermissions();

    const location =

        useLocation();

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

    if (

        allowed

    ) {

        return children;

    }

    return (

        <Navigate

            to="/unauthorized"

            replace

            state={{

                from: location,

            }}

        />

    );

}