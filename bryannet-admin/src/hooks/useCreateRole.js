import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    createRole,

} from "../api/roles";

export function useCreateRole(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: createRole,

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