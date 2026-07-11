import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    updateAdminActivation,
} from "../api/adminUsers";

export function useUpdateAdminActivation() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: ({

            adminUserId,

            isActive,

        }) =>

            updateAdminActivation(

                adminUserId,

                isActive,

            ),

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "admin-users",
                ],

            });

        },

    });

}