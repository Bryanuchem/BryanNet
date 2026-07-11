import {

    useQuery,

} from "@tanstack/react-query";

import {

    getRolePermissions,

} from "../api/permissions";

export function useRolePermissions(

    roleId,

) {

    return useQuery({

        queryKey: [

            "role-permissions",

            roleId,

        ],

        queryFn: () =>

            getRolePermissions(

                roleId,

            ),

        enabled: !!roleId,

    });

}