import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    activateCustomer,
} from "../api/customers";

export function useActivateCustomer() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: activateCustomer,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "customers",
                ],

            });

        },

    });

}