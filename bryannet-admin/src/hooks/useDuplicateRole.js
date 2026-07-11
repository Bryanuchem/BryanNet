import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    duplicateRole,

} from "../api/roles";

export function useDuplicateRole(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: duplicateRole,

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