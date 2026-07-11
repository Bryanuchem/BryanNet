import {

    useMemo,

} from "react";

import {

    useCurrentAdmin,

} from "./useCurrentAdmin";

import {

    hasPermission,

    hasAnyPermission,

    hasAllPermissions,

} from "../utils/permissions";

export function useCurrentPermissions() {

    const {

        data: admin,

        isLoading,

    } = useCurrentAdmin();

    const permissions =

        useMemo(

            () =>

                admin?.permissions ??

                [],

            [

                admin,

            ],

        );
        
    return useMemo(

        () => ({

            admin,

            permissions,

            loading:

                isLoading,

            hasPermission:

                (

                    permission,

                ) =>

                    hasPermission(

                        permissions,

                        permission,

                    ),

            hasAnyPermission:

                (

                    requiredPermissions,

                ) =>

                    hasAnyPermission(

                        permissions,

                        requiredPermissions,

                    ),

            hasAllPermissions:

                (

                    requiredPermissions,

                ) =>

                    hasAllPermissions(

                        permissions,

                        requiredPermissions,

                    ),

        }),

        [

            admin,

            permissions,

            isLoading,

        ],

    );

}