import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    updateAdminUser,
} from "../api/adminUsers";

export function useUpdateAdminUser() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: ({

            adminUserId,

            adminUser,

        }) =>

            updateAdminUser(

                adminUserId,

                adminUser,

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