import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    changeAdminRole,

} from "../api/adminUsers";

import {

    ADMIN_USERS_QUERY_KEY,

} from "./useAdminUsers";

export function useChangeAdminRole(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: ({

            adminUserId,

            roleId,

        }) =>

            changeAdminRole(

                adminUserId,

                roleId,

            ),

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:

                    ADMIN_USERS_QUERY_KEY,

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
