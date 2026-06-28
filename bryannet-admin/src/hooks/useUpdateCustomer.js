import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import { updateCustomer } from "../services/customers";

export function useUpdateCustomer() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ customerId, customerData }) =>
            updateCustomer(
                customerId,
                customerData
            ),

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["customers"],
            });
        },
    });
}