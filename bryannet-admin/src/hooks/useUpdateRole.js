import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    updateRole,

} from "../api/roles";

export function useUpdateRole(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: ({

            roleId,

            data,

        }) =>

            updateRole(

                roleId,

                data,

            ),

        onSuccess: (

            data,

            variables,

            context,

        ) => {

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