import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createAdminUser,
} from "../api/adminUsers";

export function useCreateAdminUser() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            createAdminUser,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "admin-users",
                ],

            });

        },

    });

}