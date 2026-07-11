import {

    useMutation,

    useQueryClient,

} from "@tanstack/react-query";

import {

    revokeAdminSession,

} from "../api/adminSessions";

export function useRevokeSession({

    onSuccess,

    onError,

} = {}) {

    const queryClient =

        useQueryClient();

    return useMutation({

        mutationFn:

            revokeAdminSession,

        onSuccess: (

            data,

        ) => {

            queryClient.invalidateQueries({

                queryKey: [

                    "admin-sessions",

                ],

            });

            queryClient.invalidateQueries({

                queryKey: [

                    "administration-overview",

                ],

            });

            onSuccess?.(

                data,

            );

        },

        onError: (

            error,

        ) => {

            onError?.(

                error,

            );

        },

    });

}