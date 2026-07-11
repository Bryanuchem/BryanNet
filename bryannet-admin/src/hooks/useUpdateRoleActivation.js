import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    updateRoleActivation,

} from "../api/roles";

export function useUpdateRoleActivation(

    options = {},

) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn: ({

            roleId,

            isActive,

        }) =>

            updateRoleActivation(

                roleId,

                isActive,

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