import { useMutation, useQueryClient } from "@tanstack/react-query";

import { registerCustomer } from "../services/customers";

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