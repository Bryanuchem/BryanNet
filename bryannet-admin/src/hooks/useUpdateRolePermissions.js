import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    updateRolePermissions,

} from "../api/permissions";

export function useUpdateRolePermissions(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: ({

            roleId,

            permissionIds,

        }) =>

            updateRolePermissions(

                roleId,

                permissionIds,

            ),

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey: [

                    "role-permissions",

                    variables.roleId,

                ],

            });

            queryClient.invalidateQueries({

                queryKey: [

                    "roles",

                ],

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}