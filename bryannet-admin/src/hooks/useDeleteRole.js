import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    deleteRole,

} from "../api/roles";

export function useDeleteRole(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: deleteRole,

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