import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    updatePayment,
} from "../api/payments";

export default function useUpdatePayment() {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: ({
            paymentId,
            paymentData,
        }) =>
            updatePayment(
                paymentId,
                paymentData,
            ),

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["payments"],
            });

        },

    });

}