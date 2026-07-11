import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    changeAdminPassword,
} from "../api/adminUsers";

export function useChangeAdminPassword() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: ({

            adminUserId,

            password,

        }) =>

            changeAdminPassword(

                adminUserId,

                password,

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