import { useMutation, useQueryClient } from "@tanstack/react-query";

import { registerCustomer } from "../api/customers";

export function useCreateCustomer() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: registerCustomer,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["customers"],
            });
        },
    });
}