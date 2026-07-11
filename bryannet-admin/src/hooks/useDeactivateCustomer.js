import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    deactivateCustomer,
} from "../api/customers";

export function useDeactivateCustomer() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: deactivateCustomer,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "customers",
                ],

            });

        },

    });

}